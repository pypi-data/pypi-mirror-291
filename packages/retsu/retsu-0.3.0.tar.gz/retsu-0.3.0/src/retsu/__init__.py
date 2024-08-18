"""Retsu."""

from importlib import metadata as importlib_metadata

from retsu.core import (
    MultiProcess,
    Process,
    ProcessManager,
    SingleProcess,
)
from retsu.results import (
    ResultProcessManager,
)


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.3.0"  # semantic-release


version = get_version()

__version__ = version
__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "MultiProcess",
    "ResultProcessManager",
    "SingleProcess",
    "Process",
    "ProcessManager",
]
