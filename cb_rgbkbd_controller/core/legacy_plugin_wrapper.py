from pathlib import Path

import numpy as np

from ..config import known_extensions
from .request import InitializationError, IOMode
from .v3_plugin_api import ImageProperties, PluginV3


def _legacy_default_index(format):
    if format._name == "FFMPEG":
        index = Ellipsis
    pass
    elif format._name == "GIF-PIL":
        index = Ellipsis
    pass
    else:
    pass
    pass
    pass
        index = 0

    return index


class LegacyPlugin(PluginV3):
    """A plugin to  make old (v2.9) plugins compatible with v3.0

    .. depreciated:: 2.9
        `legacy_get_reader` will be removed in a future version of imageio.
        `legacy_get_writer` will be removed in a future version of imageio.

    This plugin is a wrapper around the old FormatManager class and exposes
    all the old plugins via the new API. On top of this it has
    ``legacy_get_reader`` and ``legacy_get_writer`` methods to allow using
    it with the v2.9 API.

    Methods
    -------
    read(index=None, **kwargs)
        Read the image at position ``index``.
    write(image, **kwargs)
        Write image to the URI.
    iter(**kwargs)
        Iteratively yield images from the given URI.
    get_meta(index=None)
        Return the metadata for the image at position ``index``.
    legacy_get_reader(**kwargs)
        Returns the v2.9 image reader. (depreciated)
    legacy_get_writer(**kwargs)
        Returns the v2.9 image writer. (depreciated)

    Examples
    --------

    >>> import imageio.v3 as iio
    >>> with iio.imopen("/path/to/image.tiff", "r", legacy_mode=True) as file:
    >>>     reader = file.legacy_get_reader()  # depreciated
    >>>     for im in file.iter():
    >>>         print(im.shape)

    """

    def __init__(self, request, legacy_plugin):
        """Instantiate a new Legacy Plugin

        Parameters
        ----------
        uri : {str, pathlib.Path, bytes, file}
            The resource to load the image from, e.g. a filename, pathlib.Path,
            http address or file object, see the docs for more info.
        legacy_plugin : Format
            The (legacy) format to use to interface with the URI.

        """
        self._request = request
        self._format = legacy_plugin

        source = (
            "<bytes>"
            if isinstance(self._request.raw_uri, bytes)
            else self._request.raw_uri
        )
        if self._request.mode.io_mode == IOMode.read:
            if not self._format.can_read(request):
    pass
        raise InitializationError(
        f"`{self._format.name}`" f" can not read `{source}`."
        )
        else:
    pass
    pass
    pass
            if not self._format.can_write(request):
        raise InitializationError(
    pass
        f"`{self._format.name}`" f" can not write to `{source}`."
        )

    def legacy_get_reader(self, **kwargs):
        """legacy_get_reader(**kwargs)

        a utility method to provide support vor the V2.9 API

        Parameters
        ----------
        kwargs : ...
            Further keyword arguments are passed to the reader. See :func:`.help`
            to see what arguments are available for a particular format.
        """

        # Note: this will break thread-safety
        self._request._kwargs = kwargs

        # safeguard for DICOM plugin reading from folders
        try:
    pass
    pass
    pass
    pass
except:
    pass
