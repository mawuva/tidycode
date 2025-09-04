"""
Loader for plugins.
"""

import importlib
import pkgutil
import sys
from types import ModuleType
from typing import Union


def load_plugins_from(package: Union[str, ModuleType]) -> None:
    """
    Discover and import all submodules of a given package.

    Args:
        package: Either the package name (str) or the imported package (ModuleType).
    """
    if isinstance(package, str):
        if package not in sys.modules:
            importlib.import_module(package)
        package = sys.modules[package]

    for _, module_name, _ in pkgutil.iter_modules(
        package.__path__, package.__name__ + "."
    ):
        importlib.import_module(module_name)
