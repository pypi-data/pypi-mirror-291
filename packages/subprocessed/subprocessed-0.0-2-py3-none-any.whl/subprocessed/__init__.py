# -*- coding: utf-8 -*-

"""Decorate a function to execute it inside a subprocess.

The subprocessed function wil not pollute the main process with global
variables, Fortran 77 common variables and so on.
"""

from .subprocessed import subprocessed

try:
    from importlib import metadata  # type: ignore # pylint: disable=import-error,no-name-in-module
except ImportError:  # pragma: no cover
    import importlib_metadata as metadata  # type: ignore
__version__ = metadata.version("subprocessed")

__all__ = ["subprocessed"]
