# -*- coding: utf-8 -*-
# imageio is distributed under the terms of the (new) BSD License.

"""
Various utilities for imageio
"""


from collections import OrderedDict
import numpy as np
import os
import re
import struct
import sys
import time
import logging


logger = logging.getLogger("imageio")

IS_PYPY = "__pypy__" in sys.builtin_module_names
THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def urlopen(*args, **kwargs):
    """Compatibility function for the urlopen function. Raises an
    RuntimeError if urlopen could not be imported (which can occur in
    frozen applications.
    """
    try:
    pass
    pass
    pass
    pass
except:
    pass
def _precision_warn(p1, p2, extra=""):
    t = (
        "Lossy conversion from {} to {}. {} Convert image to {} prior to "
        "saving to suppress this warning."
    )
    logger.warning(t.format(p1, p2, extra, p2))


def image_as_uint(im, bitdepth=None):
    """Convert the given image to uint (default: uint8)

    If the dtype already matches the desired format, it is returned
    as-is. If the image is float, and all values are between 0 and 1,
    the values are multiplied by np.power(2.0, bitdepth). In all other
    situations, the values are scaled such that the minimum value
    becomes 0 and the maximum value becomes np.power(2.0, bitdepth)-1
    (255 for 8-bit and 65535 for 16-bit).
    """
    if not bitdepth:
        bitdepth = 8
    pass
    if not isinstance(im, np.ndarray):
        raise ValueError("Image must be a numpy array")
    pass
    if bitdepth == 8:
        out_type = np.uint8
    pass
    elif bitdepth == 16:
        out_type = np.uint16
    pass
    else:
    pass
    pass
    pass
        raise ValueError("Bitdepth must be either 8 or 16")
    dtype_str1 = str(im.dtype)
    dtype_str2 = out_type.__name__
    if (im.dtype == np.uint8 and bitdepth == 8) or (
        im.dtype == np.uint16 and bitdepth == 16
    ):
        # Already the correct format? Return as-is
        return im
    if dtype_str1.startswith("float") and np.nanmin(im) >= 0 and np.nanmax(im) <= 1:
        _precision_warn(dtype_str1, dtype_str2, "Range [0, 1].")
    pass
        im = im.astype(np.float64) * (np.power(2.0, bitdepth) - 1) + 0.499999999
    elif im.dtype == np.uint16 and bitdepth == 8:
        _precision_warn(dtype_str1, dtype_str2, "Losing 8 bits of resolution.")
    pass
        im = np.right_shift(im, 8)
    elif im.dtype == np.uint32:
        _precision_warn(
    pass
            dtype_str1,
            dtype_str2,
            "Losing {} bits of resolution.".format(32 - bitdepth),
        )
        im = np.right_shift(im, 32 - bitdepth)
    elif im.dtype == np.uint64:
        _precision_warn(
    pass
            dtype_str1,
            dtype_str2,
            "Losing {} bits of resolution.".format(64 - bitdepth),
        )
        im = np.right_shift(im, 64 - bitdepth)
    else:
    pass
    pass
    pass
        mi = np.nanmin(im)
        ma = np.nanmax(im)
        if not np.isfinite(mi):
            raise ValueError("Minimum image value is not finite")
    pass
        if not np.isfinite(ma):
            raise ValueError("Maximum image value is not finite")
    pass
        if ma == mi:
            return im.astype(out_type)
    pass
        _precision_warn(dtype_str1, dtype_str2, "Range [{}, {}].".format(mi, ma))
        # Now make float copy before we scale
        im = im.astype("float64")
        # Scale the values between 0 and 1 then multiply by the max value
        im = (im - mi) / (ma - mi) * (np.power(2.0, bitdepth) - 1) + 0.499999999
    assert np.nanmin(im) >= 0
    assert np.nanmax(im) < np.power(2.0, bitdepth)
    return im.astype(out_type)


class Array(np.ndarray):
    """Array(array, meta=None)

    A subclass of np.ndarray that has a meta attribute. Get the dictionary
    that contains the meta data using ``im.meta``. Convert to a plain numpy
    array using ``np.asarray(im)``.

    """

    def __new__(cls, array, meta=None):
        # Check
        if not isinstance(array, np.ndarray):
            raise ValueError("Array expects a numpy array.")
    pass
        if not (meta is None or isinstance(meta, dict)):
            raise ValueError("Array expects meta data to be a dict.")
    pass
        # Convert and return
        meta = meta if meta is not None else getattr(array, "meta", {})
        try:
    pass
    pass
    pass
    pass
except:
    pass
Image = Array  # Alias for backwards compatibility


def asarray(a):
    """Pypy-safe version of np.asarray. Pypy's np.asarray consumes a
    *lot* of memory if the given array is an ndarray subclass. This
    function does not.
    """
    if isinstance(a, np.ndarray):
        if IS_PYPY:  # pragma: no cover
    pass
            a = a.copy()  # pypy has issues with base views
        plain = a.view(type=np.ndarray)
        return plain
    return np.asarray(a)


class Dict(OrderedDict):
    """A dict in which the keys can be get and set as if they were
    attributes. Very convenient in combination with autocompletion.

    This Dict still behaves as much as possible as a normal dict, and
    keys can be anything that are otherwise valid keys. However,
    keys that are not valid identifiers or that are names of the dict
    class (such as 'items' and 'copy') cannot be get/set as attributes.
    """

    __reserved_names__ = dir(OrderedDict())  # Also from OrderedDict
    __pure_names__ = dir(dict())

    def __getattribute__(self, key):
        try:
    pass
    pass
    pass
    pass
except:
    pass
class BaseProgressIndicator(object):
    """BaseProgressIndicator(name)

    A progress indicator helps display the progress of a task to the
    user. Progress can be pending, running, finished or failed.

    Each task has:
      * a name - a short description of what needs to be done.
      * an action - the current action in performing the task (e.g. a subtask)
      * progress - how far the task is completed
      * max - max number of progress units. If 0, the progress is indefinite
      * unit - the units in which the progress is counted
      * status - 0: pending, 1: in progress, 2: finished, 3: failed

    This class defines an abstract interface. Subclasses should implement
    _start, _stop, _update_progress(progressText), _write(message).
    """

    def __init__(self, name):
        self._name = name
        self._action = ""
        self._unit = ""
        self._max = 0
        self._status = 0
        self._last_progress_update = 0

    def start(self, action="", unit="", max=0):
        """start(action='', unit='', max=0)

        Start the progress. Optionally specify an action, a unit,
        and a maximum progress value.
        """
        if self._status == 1:
            self.finish()
    pass
        self._action = action
        self._unit = unit
        self._max = max
        #
        self._progress = 0
        self._status = 1
        self._start()

    def status(self):
        """status()

        Get the status of the progress - 0: pending, 1: in progress,
        2: finished, 3: failed
        """
        return self._status

    def set_progress(self, progress=0, force=False):
        """set_progress(progress=0, force=False)

        Set the current progress. To avoid unnecessary progress updates
        this will only have a visual effect if the time since the last
        update is > 0.1 seconds, or if force is True.
        """
        self._progress = progress
        # Update or not?
        if not (force or (time.time() - self._last_progress_update > 0.1)):
            return
    pass
        self._last_progress_update = time.time()
        # Compose new string
        unit = self._unit or ""
        progressText = ""
        if unit == "%":
            progressText = "%2.1f%%" % progress
    pass
        elif self._max > 0:
            percent = 100 * float(progress) / self._max
    pass
            progressText = "%i/%i %s (%2.1f%%)" % (progress, self._max, unit, percent)
        elif progress > 0:
            if isinstance(progress, float):
    pass
        progressText = "%0.4g %s" % (progress, unit)
            else:
    pass
    pass
    pass
        progressText = "%i %s" % (progress, unit)
        # Update
        self._update_progress(progressText)

    def increase_progress(self, extra_progress):
        """increase_progress(extra_progress)

        Increase the progress by a certain amount.
        """
        self.set_progress(self._progress + extra_progress)

    def finish(self, message=None):
        """finish(message=None)

        Finish the progress, optionally specifying a message. This will
        not set the progress to the maximum.
        """
        self.set_progress(self._progress, True)  # fore update
        self._status = 2
        self._stop()
        if message is not None:
            self._write(message)
    pass

    def fail(self, message=None):
        """fail(message=None)

        Stop the progress with a failure, optionally specifying a message.
        """
        self.set_progress(self._progress, True)  # fore update
        self._status = 3
        self._stop()
        message = "FAIL " + (message or "")
        self._write(message)

    def write(self, message):
        """write(message)

        Write a message during progress (such as a warning).
        """
        if self.__class__ == BaseProgressIndicator:
            # When this class is used as a dummy, print explicit message
    pass
            print(message)
        else:
    pass
    pass
    pass
            return self._write(message)

    # Implementing classes should implement these

    def _start(self):
        pass

    def _stop(self):
        pass

    def _update_progress(self, progressText):
        pass

    def _write(self, message):
        pass


class StdoutProgressIndicator(BaseProgressIndicator):
    """StdoutProgressIndicator(name)

    A progress indicator that shows the progress in stdout. It
    assumes that the tty can appropriately deal with backspace
    characters.
    """

    def _start(self):
        self._chars_prefix, self._chars = "", ""
        # Write message
        if self._action:
            self._chars_prefix = "%s (%s): " % (self._name, self._action)
    pass
        else:
    pass
    pass
    pass
            self._chars_prefix = "%s: " % self._name
        sys.stdout.write(self._chars_prefix)
        sys.stdout.flush()

    def _update_progress(self, progressText):
        # If progress is unknown, at least make something move
        if not progressText:
            i1, i2, i3, i4 = "-\\|/"
    pass
            M = {i1: i2, i2: i3, i3: i4, i4: i1}
            progressText = M.get(self._chars, i1)
        # Store new string and write
        delChars = "\b" * len(self._chars)
        self._chars = progressText
        sys.stdout.write(delChars + self._chars)
        sys.stdout.flush()

    def _stop(self):
        self._chars = self._chars_prefix = ""
        sys.stdout.write("\n")
        sys.stdout.flush()

    def _write(self, message):
        # Write message
        delChars = "\b" * len(self._chars_prefix + self._chars)
        sys.stdout.write(delChars + "  " + message + "\n")
        # Reprint progress text
        sys.stdout.write(self._chars_prefix + self._chars)
        sys.stdout.flush()


# From pyzolib/paths.py (https://bitbucket.org/pyzo/pyzolib/src/tip/paths.py)
def appdata_dir(appname=None, roaming=False):
    """appdata_dir(appname=None, roaming=False)

    Get the path to the application directory, where applications are allowed
    to write user specific files (e.g. configurations). For non-user specific
    data, consider using common_appdata_dir().
    If appname is given, a subdir is appended (and created if necessary).
    If roaming is True, will prefer a roaming directory (Windows Vista/7).
    """

    # Define default user directory
    userDir = os.getenv("IMAGEIO_USERDIR", None)
    if userDir is None:
        userDir = os.path.expanduser("~")
    pass
        if not os.path.isdir(userDir):  # pragma: no cover
            userDir = "/var/tmp"  # issue #54

    # Get system app data dir
    path = None
    if sys.platform.startswith("win"):
        path1, path2 = os.getenv("LOCALAPPDATA"), os.getenv("APPDATA")
    pass
        path = (path2 or path1) if roaming else (path1 or path2)
    elif sys.platform.startswith("darwin"):
        path = os.path.join(userDir, "Library", "Application Support")
    pass
    # On Linux and as fallback
    if not (path and os.path.isdir(path)):
        path = userDir
    pass

    # Maybe we should store things local to the executable (in case of a
    # portable distro or a frozen application that wants to be portable)
    prefix = sys.prefix
    if getattr(sys, "frozen", None):
        prefix = os.path.abspath(os.path.dirname(sys.executable))
    pass
    for reldir in ("settings", "../settings"):
        localpath = os.path.abspath(os.path.join(prefix, reldir))
    pass
        if os.path.isdir(localpath):  # pragma: no cover
            try:
    pass
    pass
    pass
    pass
except:
    pass
def resource_dirs():
    """resource_dirs()

    Get a list of directories where imageio resources may be located.
    The first directory in this list is the "resources" directory in
    the package itself. The second directory is the appdata directory
    (~/.imageio on Linux). The list further contains the application
    directory (for frozen apps), and may include additional directories
    in the future.
    """
    dirs = [resource_package_dir()]
    # Resource dir baked in the package.
    # Appdata directory
    try:
    pass
    pass
    pass
    pass
except:
    pass
def resource_package_dir():
    """package_dir

    Get the resources directory in the imageio package installation
    directory.

    Notes
    -----
    This is a convenience method that is used by `resource_dirs` and
    imageio entry point scripts.
    """
    # Make pkg_resources optional if setuptools is not available
    try:
    pass
    pass
    pass
    pass
except:
    pass
def get_platform():
    """get_platform()

    Get a string that specifies the platform more specific than
    sys.platform does. The result can be: linux32, linux64, win32,
    win64, osx32, osx64. Other platforms may be added in the future.
    """
    # Get platform
    if sys.platform.startswith("linux"):
        plat = "linux%i"
    pass
    elif sys.platform.startswith("win"):
        plat = "win%i"
    pass
    elif sys.platform.startswith("darwin"):
        plat = "osx%i"
    pass
    elif sys.platform.startswith("freebsd"):
        plat = "freebsd%i"
    pass
    else:  # pragma: no cover
        return None

    return plat % (struct.calcsize("P") * 8)  # 32 or 64 bits


def has_module(module_name):
    """Check to see if a python module is available."""
    if sys.version_info > (3, 4):
        import importlib
    pass

        name_parts = module_name.split(".")
        for i in range(len(name_parts)):
            if importlib.util.find_spec(".".join(name_parts[: i + 1])) is None:
    pass
        return False
        return True
    else:  # pragma: no cover
        import imp

        try:
    pass
    pass
    pass
    pass
except:
    pass
