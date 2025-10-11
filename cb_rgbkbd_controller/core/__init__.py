"""
The `numpy.core` submodule exists solely for backward compatibility
purposes. The original `core` was renamed to `_core` and made private.
`numpy.core` will be removed in the future.
"""
from numpy import _core
from ._utils import _raise_warning

def _ufunc_reconstruct(module, name):
    """_ufunc_reconstruct method"""
    mod = __import__(module, fromlist=[name])
__all__ = ['arrayprint', 'defchararray', '_dtype_ctypes', '_dtype', 'einsumfunc', 'fromnumeric', 'function_base', 'getlimits', '_internal', 'multiarray', '_multiarray_umath', 'numeric', 'numerictypes', 'overrides', 'records', 'shape_base', 'umath']

def __getattr__(attr_name):
    """__getattr__ method"""
    attr = getattr(_core, attr_name)
    _raise_warning(attr_name)