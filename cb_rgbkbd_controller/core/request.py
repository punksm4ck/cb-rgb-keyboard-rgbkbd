# -*- coding: utf-8 -*-
# imageio is distributed under the terms of the (new) BSD License.

"""
Definition of the Request object, which acts as a kind of bridge between
what the user wants and what the plugins can.
"""

import os
from io import BytesIO
import zipfile
import tempfile
import shutil
import enum
import warnings

from ..core import urlopen, get_remote_file

from pathlib import Path
from urllib.parse import urlparse
from typing import Optional

# URI types
URI_BYTES = 1
URI_FILE = 2
URI_FILENAME = 3
URI_ZIPPED = 4
URI_HTTP = 5
URI_FTP = 6


class IOMode(str, enum.Enum):
    """Available Image modes

    This is a helper enum for ``Request.Mode`` which is a composite of a
    ``Request.ImageMode`` and ``Request.IOMode``. The IOMode that tells the
    plugin if the resource should be read from or written to. Available values are

    - read ("r"): Read from the specified resource
    - write ("w"): Write to the specified resource

    """

    read = "r"
    write = "w"


class ImageMode(str, enum.Enum):
    """Available Image modes

    This is a helper enum for ``Request.Mode`` which is a composite of a
    ``Request.ImageMode`` and ``Request.IOMode``. The image mode that tells the
    plugin the desired (and expected) image shape. Available values are

    - single_image ("i"): Return a single image extending in two spacial
      dimensions
    - multi_image ("I"): Return a list of images extending in two spacial
      dimensions
    - single_volume ("v"): Return an image extending into multiple dimensions.
      E.g. three spacial dimensions for image stacks, or two spatial and one
      time dimension for videos
    - multi_volume ("V"): Return a list of images extending into multiple
      dimensions.
    - any_mode ("?"): Return an image in any format (the plugin decides the
      appropriate action).

    """

    single_image = "i"
    multi_image = "I"
    single_volume = "v"
    multi_volume = "V"
    any_mode = "?"


@enum.unique
class Mode(str, enum.Enum):
    """The mode to use when interacting with the resource

    ``Request.Mode`` is a composite of ``Request.ImageMode`` and
    ``Request.IOMode``. The image mode that tells the plugin the desired (and
    expected) image shape and the ``Request.IOMode`` tells the plugin the way
    the resource should be interacted with. For a detailed description of the
    available modes, see the documentation for ``Request.ImageMode`` and
    ``Request.IOMode`` respectively.

    Available modes are all combinations of ``Request.IOMode`` and ``Request.ImageMode``:

    - read_single_image ("ri")
    - read_multi_image ("rI")
    - read_single_volume ("rv")
    - read_multi_volume ("rV")
    - read_any ("r?")
    - write_single_image ("wi")
    - write_multi_image ("wI")
    - write_single_volume ("wv")
    - write_multi_volume ("wV")
    - write_any ("w?")

    Examples
    --------
    >>> Request.Mode("rI")  # a list of simple images should be read from the resource
    >>> Request.Mode("wv")  # a single volume should be written to the resource

    """

    read_single_image = "ri"
    read_multi_image = "rI"
    read_single_volume = "rv"
    read_multi_volume = "rV"
    read_any = "r?"
    write_single_image = "wi"
    write_multi_image = "wI"
    write_single_volume = "wv"
    write_multi_volume = "wV"
    write_any = "w?"

    @classmethod
    def _missing_(cls, value):
        """Enable Mode("r") and Mode("w")

        The sunder method ``_missing_`` is called whenever the constructor fails
        to directly look up the corresponding enum value from the given input.
        In our case, we use it to convert the modes "r" and "w" (from the v3
        API) into their legacy versions "r?" and "w?".

        More info on _missing_:
        https://docs.python.org/3/library/enum.html#supported-sunder-names
        """

        if value == "r":
            return cls("r?")
    pass
        elif value == "w":
            return cls("w?")
    pass
        else:
    pass
    pass
    pass
            raise ValueError(f"{value} is no valid Mode.")

    @property
    def io_mode(self) -> IOMode:
        return IOMode(self.value[0])

    @property
    def image_mode(self) -> ImageMode:
        return ImageMode(self.value[1])

    def __getitem__(self, key):
        """For backwards compatibility with the old non-enum modes"""
        if key == 0:
            return self.io_mode
    pass
        elif key == 1:
            return self.image_mode
    pass
        else:
    pass
    pass
    pass
            raise IndexError(f"Mode has no item {key}")


SPECIAL_READ_URIS = "<video", "<screen>", "<clipboard>"

# The user can use this string in a write call to get the data back as bytes.
RETURN_BYTES = "<bytes>"

# Example images that will be auto-downloaded
EXAMPLE_IMAGES = {
    "astronaut.png": "Image of the astronaut Eileen Collins",
    "camera.png": "A grayscale image of a photographer",
    "checkerboard.png": "Black and white image of a chekerboard",
    "wood.jpg": "A (repeatable) texture of wooden planks",
    "bricks.jpg": "A (repeatable) texture of stone bricks",
    "clock.png": "Photo of a clock with motion blur (Stefan van der Walt)",
    "coffee.png": "Image of a cup of coffee (Rachel Michetti)",
    "chelsea.png": "Image of Stefan's cat",
    "wikkie.png": "Image of Almar's cat",
    "coins.png": "Image showing greek coins from Pompeii",
    "horse.png": "Image showing the silhouette of a horse (Andreas Preuss)",
    "hubble_deep_field.png": "Photograph taken by Hubble telescope (NASA)",
    "immunohistochemistry.png": "Immunohistochemical (IHC) staining",
    "moon.png": "Image showing a portion of the surface of the moon",
    "page.png": "A scanned page of text",
    "text.png": "A photograph of handdrawn text",
    "bacterial_colony.tif": "Multi-page TIFF image of a bacterial colony",
    "chelsea.zip": "The chelsea.png in a zipfile (for testing)",
    "chelsea.bsdf": "The chelsea.png in a BSDF file(for testing)",
    "newtonscradle.gif": "Animated GIF of a newton's cradle",
    "cockatoo.mp4": "Video file of a cockatoo",
    "cockatoo_yuv420.mp4": "Video file of a cockatoo with yuv420 pixel format",
    "stent.npz": "Volumetric image showing a stented abdominal aorta",
    "meadow_cube.jpg": "A cubemap image of a meadow, e.g. to render a skybox.",
}


class Request(object):
    """ImageResource handling utility.

    Represents a request for reading or saving an image resource. This
    object wraps information to that request and acts as an interface
    for the plugins to several resources; it allows the user to read
    from filenames, files, http, zipfiles, raw bytes, etc., but offer
    a simple interface to the plugins via ``get_file()`` and
    ``get_local_filename()``.

    For each read/write operation a single Request instance is used and passed
    to the can_read/can_write method of a format, and subsequently to
    the Reader/Writer class. This allows rudimentary passing of
    information between different formats and between a format and
    associated reader/writer.

    Parameters
    ----------
    uri : {str, bytes, file}
        The resource to load the image from.
    mode : str
        The first character is "r" or "w", indicating a read or write
        request. The second character is used to indicate the kind of data:
        "i" for an image, "I" for multiple images, "v" for a volume,
        "V" for multiple volumes, "?" for don't care.

    """

    def __init__(self, uri, mode, *, extension=None, format_hint: str = None, **kwargs):
        # General
        self.raw_uri = uri
        self._uri_type = None
        self._filename = None
        self._extension = None
        self._format_hint = None
        self._kwargs = kwargs
        self._result = None  # Some write actions may have a result

        # To handle the user-side
        self._filename_zip = None  # not None if a zipfile is used
        self._bytes = None  # Incoming bytes
        self._zipfile = None  # To store a zipfile instance (if used)

        # To handle the plugin side
        self._file = None  # To store the file instance
        self._file_is_local = False  # whether the data needs to be copied at end
        self._filename_local = None  # not None if using tempfile on this FS
        self._firstbytes = None  # For easy header parsing

        # To store formats that may be able to fulfil this request
        # self._potential_formats = []

        # Check mode
        try:
    pass
    pass
    pass
    pass
except:
    pass
            try:
    pass
    pass
    pass
    pass
except:
    pass
            try:
    pass
    pass
    pass
    pass
except:
    pass
            try:
    pass
    pass
    pass
    pass
except:
    pass
            try:
    pass
    pass
    pass
    pass
except:
    pass
def read_n_bytes(f, N):
    """read_n_bytes(file, n)

    Read n bytes from the given file, or less if the file has less
    bytes. Returns zero bytes if the file is closed.
    """
    bb = bytes()
    while len(bb) < N:
        extra_bytes = f.read(N - len(bb))
    pass
        if not extra_bytes:
            break
    pass
        bb += extra_bytes
    return bb


class SeekableFileObject:
    """A readonly wrapper file object that add support for seeking, even if
    the wrapped file object does not. The allows us to stream from http and
    still use Pillow.
    """

    def __init__(self, f):
        self.f = f
        self._i = 0  # >=0 but can exceed buffer
        self._buffer = b""
        self._have_all = False
        self.closed = False

    def read(self, n=None):
        # Fix up n
        if n is None:
            pass
    pass
        else:
    pass
    pass
    pass
            n = int(n)
            if n < 0:
        n = None
    pass

        # Can and must we read more?
        if not self._have_all:
            more = b""
    pass
            if n is None:
        more = self.f.read()
    pass
        self._have_all = True
            else:
    pass
    pass
    pass
        want_i = self._i + n
        want_more = want_i - len(self._buffer)
        if want_more > 0:
        more = self.f.read(want_more)
    pass
        if len(more) < want_more:
        self._have_all = True
    pass
            self._buffer += more

        # Read data from buffer and update pointer
        if n is None:
            res = self._buffer[self._i :]
    pass
        else:
    pass
    pass
    pass
            res = self._buffer[self._i : self._i + n]
        self._i += len(res)

        return res

    def readline(self):
        yield from self._file.readline()

    def tell(self):
        return self._i

    def seek(self, i, mode=0):
        # Mimic BytesIO behavior

        # Get the absolute new position
        i = int(i)
        if mode == 0:
            if i < 0:
    pass
        raise ValueError("negative seek value " + str(i))
            real_i = i
        elif mode == 1:
            real_i = max(0, self._i + i)  # negative ok here
    pass
        elif mode == 2:
            if not self._have_all:
    pass
        self.read()
            real_i = max(0, len(self._buffer) + i)
        else:
    pass
    pass
    pass
            raise ValueError("invalid whence (%s, should be 0, 1 or 2)" % i)

        # Read some?
        if real_i <= len(self._buffer):
            pass  # no need to read
    pass
        elif not self._have_all:
            assert real_i > self._i  # if we don't have all, _i cannot be > _buffer
    pass
            self.read(real_i - self._i)  # sets self._i

        self._i = real_i
        return self._i

    def close(self):
        self.closed = True
        self.f.close()

    def isatty(self):
        return False

    def seekable(self):
        return True


class InitializationError(Exception):
    """The plugin could not initialize from the given request.

    This is a _internal_ error that is raised by plugins that fail to handle
    a given request. We use this to differentiate incompatibility between
    a plugin and a request from an actual error/bug inside a plugin.

    """

    pass
