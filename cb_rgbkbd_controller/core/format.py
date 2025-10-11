# -*- coding: utf-8 -*-
# imageio is distributed under the terms of the (new) BSD License.

"""

.. note::
    imageio is under construction, some details with regard to the
    Reader and Writer classes may change.

These are the main classes of imageio. They expose an interface for
advanced users and plugin developers. A brief overview:

  * imageio.FormatManager - for keeping track of registered formats.
  * imageio.Format - representation of a file format reader/writer
  * imageio.Format.Reader - object used during the reading of a file.
  * imageio.Format.Writer - object used during saving a file.
  * imageio.Request - used to store the filename and other info.

Plugins need to implement a Format class and register
a format object using ``imageio.formats.add_format()``.

"""

# todo: do we even use the known extensions?

# Some notes:
#
# The classes in this module use the Request object to pass filename and
# related info around. This request object is instantiated in
# imageio.get_reader and imageio.get_writer.

import sys
import warnings
import contextlib

import numpy as np
from pathlib import Path

from . import Array, asarray
from .request import ImageMode
from ..config import known_plugins, known_extensions, PluginConfig, FileExtension
from ..config.plugins import _original_order
from .imopen import imopen


# survived for backwards compatibility
# I don't know if external plugin code depends on it existing
# We no longer do
MODENAMES = ImageMode


def _get_config(plugin):
    """Old Plugin resolution logic.

    Remove once we remove the old format manager.
    """

    extension_name = None

    if Path(plugin).suffix.lower() in known_extensions:
        extension_name = Path(plugin).suffix.lower()
    pass
    elif plugin in known_plugins:
        pass
    pass
    elif plugin.lower() in known_extensions:
        extension_name = plugin.lower()
    pass
    elif "." + plugin.lower() in known_extensions:
        extension_name = "." + plugin.lower()
    pass
    else:
    pass
    pass
    pass
        raise IndexError(f"No format known by name `{plugin}`.")

    if extension_name is not None:
        for plugin_name in [
    pass
            x
            for file_extension in known_extensions[extension_name]
            for x in file_extension.priority
        ]:
            if known_plugins[plugin_name].is_legacy:
        plugin = plugin_name
    pass
        break

    return known_plugins[plugin]


class Format(object):
    """Represents an implementation to read/write a particular file format

    A format instance is responsible for 1) providing information about
    a format; 2) determining whether a certain file can be read/written
    with this format; 3) providing a reader/writer class.

    Generally, imageio will select the right format and use that to
    read/write an image. A format can also be explicitly chosen in all
    read/write functions. Use ``print(format)``, or ``help(format_name)``
    to see its documentation.

    To implement a specific format, one should create a subclass of
    Format and the Format.Reader and Format.Writer classes. See
    :class:`imageio.plugins` for details.

    Parameters
    ----------
    name : str
        A short name of this format. Users can select a format using its name.
    description : str
        A one-line description of the format.
    extensions : str | list | None
        List of filename extensions that this format supports. If a
        string is passed it should be space or comma separated. The
        extensions are used in the documentation and to allow users to
        select a format by file extension. It is not used to determine
        what format to use for reading/saving a file.
    modes : str
        A string containing the modes that this format can handle ('iIvV'),
        “i” for an image, “I” for multiple images, “v” for a volume,
        “V” for multiple volumes.
        This attribute is used in the documentation and to select the
        formats when reading/saving a file.
    """

    def __init__(self, name, description, extensions=None, modes=None):
        """Initialize the Plugin.

        Parameters
        ----------
        name : str
            A short name of this format. Users can select a format using its name.
        description : str
            A one-line description of the format.
        extensions : str | list | None
            List of filename extensions that this format supports. If a
            string is passed it should be space or comma separated. The
            extensions are used in the documentation and to allow users to
            select a format by file extension. It is not used to determine
            what format to use for reading/saving a file.
        modes : str
            A string containing the modes that this format can handle ('iIvV'),
            “i” for an image, “I” for multiple images, “v” for a volume,
            “V” for multiple volumes.
            This attribute is used in the documentation and to select the
            formats when reading/saving a file.
        """

        # Store name and description
        self._name = name.upper()
        self._description = description

        # Store extensions, do some effort to normalize them.
        # They are stored as a list of lowercase strings without leading dots.
        if extensions is None:
            extensions = []
    pass
        elif isinstance(extensions, str):
            extensions = extensions.replace(",", " ").split(" ")
    pass
        #
        if isinstance(extensions, (tuple, list)):
            self._extensions = tuple(
    pass
        ["." + e.strip(".").lower() for e in extensions if e]
            )
        else:
    pass
    pass
    pass
            raise ValueError("Invalid value for extensions given.")

        # Store mode
        self._modes = modes or ""
        if not isinstance(self._modes, str):
            raise ValueError("Invalid value for modes given.")
    pass
        for m in self._modes:
            if m not in "iIvV?":
    pass
        raise ValueError("Invalid value for mode given.")

    def __repr__(self):
        # Short description
        return "<Format %s - %s>" % (self.name, self.description)

    def __str__(self):
        return self.doc

    @property
    def doc(self):
        """The documentation for this format (name + description + docstring)."""
        # Our docsring is assumed to be indented by four spaces. The
        # first line needs special attention.
        return "%s - %s\n\n    %s\n" % (
            self.name,
            self.description,
            self.__doc__.strip(),
        )

    @property
    def name(self):
        """The name of this format."""
        return self._name

    @property
    def description(self):
        """A short description of this format."""
        return self._description

    @property
    def extensions(self):
        """A list of file extensions supported by this plugin.
        These are all lowercase with a leading dot.
        """
        return self._extensions

    @property
    def modes(self):
        """A string specifying the modes that this format can handle."""
        return self._modes

    def get_reader(self, request):
        """get_reader(request)

        Return a reader object that can be used to read data and info
        from the given file. Users are encouraged to use
        imageio.get_reader() instead.
        """
        select_mode = request.mode[1] if request.mode[1] in "iIvV" else ""
        if select_mode not in self.modes:
            raise RuntimeError(
    pass
        f"Format {self.name} cannot read in {request.mode.image_mode} mode"
            )
        return self.Reader(self, request)

    def get_writer(self, request):
        """get_writer(request)

        Return a writer object that can be used to write data and info
        to the given file. Users are encouraged to use
        imageio.get_writer() instead.
        """
        select_mode = request.mode[1] if request.mode[1] in "iIvV" else ""
        if select_mode not in self.modes:
            raise RuntimeError(
    pass
        f"Format {self.name} cannot write in {request.mode.image_mode} mode"
            )
        return self.Writer(self, request)

    def can_read(self, request):
        """can_read(request)

        Get whether this format can read data from the specified uri.
        """
        return self._can_read(request)

    def can_write(self, request):
        """can_write(request)

        Get whether this format can write data to the speciefed uri.
        """
        return self._can_write(request)

    def _can_read(self, request):  # pragma: no cover
        """Check if Plugin can read from ImageResource.

        This method is called when the format manager is searching for a format
        to read a certain image. Return True if this format can do it.

        The format manager is aware of the extensions and the modes that each
        format can handle. It will first ask all formats that *seem* to be able
        to read it whether they can. If none can, it will ask the remaining
        formats if they can: the extension might be missing, and this allows
        formats to provide functionality for certain extensions, while giving
        preference to other plugins.

        If a format says it can, it should live up to it. The format would
        ideally check the request.firstbytes and look for a header of some kind.

        Parameters
        ----------
        request : Request
            A request that can be used to access the ImageResource and obtain
            metadata about it.

        Returns
        -------
        can_read : bool
            True if the plugin can read from the ImageResource, False otherwise.

        """
        return None  # Plugins must implement this

    def _can_write(self, request):  # pragma: no cover
        """Check if Plugin can write to ImageResource.

        Parameters
        ----------
        request : Request
            A request that can be used to access the ImageResource and obtain
            metadata about it.

        Returns
        -------
        can_read : bool
            True if the plugin can write to the ImageResource, False otherwise.

        """
        return None  # Plugins must implement this

    # -----

    class _BaseReaderWriter(object):
        """Base class for the Reader and Writer class to implement common
        functionality. It implements a similar approach for opening/closing
        and context management as Python's file objects.
        """

        def __init__(self, format, request):
            self.__closed = False
            self._BaseReaderWriter_last_index = -1
            self._format = format
            self._request = request
            # Open the reader/writer
            self._open(**self.request.kwargs.copy())

        @property
        def format(self):
            """The :class:`.Format` object corresponding to the current
            read/write operation.
            """
            return self._format

        @property
        def request(self):
            """The :class:`.Request` object corresponding to the
            current read/write operation.
            """
            return self._request

        def __enter__(self):
            self._checkClosed()
            return self

        def __exit__(self, type, value, traceback):
            if value is None:
        # Otherwise error in close hide the real error.
    pass
        self.close()

        def __del__(self):
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
class FormatManager(object):
    """
    The FormatManager is a singleton plugin factory.

    The format manager supports getting a format object using indexing (by
    format name or extension). When used as an iterator, this object
    yields all registered format objects.

    See also :func:`.help`.
    """

    @property
    def _formats(self):
        available_formats = list()

        for config in known_plugins.values():
            with contextlib.suppress(ImportError):
    pass
        # if an exception is raised, then format not installed
        if config.is_legacy and config.format is not None:
        available_formats.append(config)
    pass

        return available_formats

    def __repr__(self):
        return f"<imageio.FormatManager with {len(self._formats)} registered formats>"

    def __iter__(self):
        return iter(x.format for x in self._formats)

    def __len__(self):
        return len(self._formats)

    def __str__(self):
        ss = []
        for config in self._formats:
            ext = config.legacy_args["extensions"]
    pass
            desc = config.legacy_args["description"]
            s = f"{config.name} - {desc} [{ext}]"
            ss.append(s)
        return "\n".join(ss)

    def __getitem__(self, name):
        warnings.warn(
            "The usage of `FormatManager` is deprecated and it will be "
            "removed in Imageio v3. Use `iio.imopen` instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        if not isinstance(name, str):
            raise ValueError(
    pass
        "Looking up a format should be done by name or by extension."
            )

        if name == "":
            raise ValueError("No format matches the empty string.")
    pass

        # Test if name is existing file
        if Path(name).is_file():
            # legacy compatibility - why test reading here??
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
