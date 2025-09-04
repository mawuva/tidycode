"""
TidyCode Plugins Loader Tests
"""

import sys
from unittest import mock

import pytest

from tidycode.plugins.loader import load_plugins_from

# ---------------------------
# Unit tests
# ---------------------------


def test_load_plugins_from_string_package():
    """
    Scenario:
        Load plugins from a package specified as string.

    Expected:
        Package is imported and submodules are loaded.
    """
    # Mock the importlib and pkgutil modules
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
                # Setup mocks
                mock_sys.modules = {}
                mock_module = mock.MagicMock()
                mock_module.__path__ = ["/path/to/package"]
                mock_module.__name__ = "test.package"
                mock_sys.modules["test.package"] = mock_module

                mock_importlib.import_module.return_value = mock_module

                # Mock pkgutil.iter_modules to return some submodules
                mock_pkgutil.iter_modules.return_value = [
                    ("", "submodule1", False),
                    ("", "submodule2", False),
                ]

                # Call the function
                load_plugins_from("test.package")

                # Verify that importlib.import_module was called for the package first
                expected_calls = [mock.call("submodule1"), mock.call("submodule2")]
                mock_importlib.import_module.assert_has_calls(expected_calls)

                # Verify that pkgutil.iter_modules was called
                mock_pkgutil.iter_modules.assert_called_with(
                    ["/path/to/package"], "test.package."
                )

                # Verify that submodules were imported
                assert (
                    mock_importlib.import_module.call_count == 2
                )  # 2 for submodules (package already in sys.modules)


def test_load_plugins_from_module_object():
    """
    Scenario:
        Load plugins from a module object.

    Expected:
        Submodules are loaded without importing the package again.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            # Create a mock module
            mock_module = mock.MagicMock()
            mock_module.__path__ = ["/path/to/package"]
            mock_module.__name__ = "test.package"

            # Mock pkgutil.iter_modules to return some submodules
            mock_pkgutil.iter_modules.return_value = [
                ("", "submodule1", False),
                ("", "submodule2", False),
            ]

            # Call the function with module object
            load_plugins_from(mock_module)

            # Verify that importlib.import_module was called for submodules only
            # (since we passed a module object, the package itself is not imported)
            expected_calls = [mock.call("submodule1"), mock.call("submodule2")]
            mock_importlib.import_module.assert_has_calls(expected_calls)

            # Verify that pkgutil.iter_modules was called
            mock_pkgutil.iter_modules.assert_called_with(
                ["/path/to/package"], "test.package."
            )


def test_load_plugins_from_empty_package():
    """
    Scenario:
        Load plugins from a package with no submodules.

    Expected:
        No submodules are imported.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
                # Setup mocks
                mock_sys.modules = {}
                mock_module = mock.MagicMock()
                mock_module.__path__ = ["/path/to/package"]
                mock_module.__name__ = "test.package"
                mock_sys.modules["test.package"] = mock_module

                mock_importlib.import_module.return_value = mock_module

                # Mock pkgutil.iter_modules to return no submodules
                mock_pkgutil.iter_modules.return_value = []

                # Call the function
                load_plugins_from("test.package")

                # Verify that importlib.import_module was not called (package already in sys.modules)
                mock_importlib.import_module.assert_not_called()

                # Verify that pkgutil.iter_modules was called
                mock_pkgutil.iter_modules.assert_called_with(
                    ["/path/to/package"], "test.package."
                )


def test_load_plugins_from_package_with_nested_modules():
    """
    Scenario:
        Load plugins from a package with nested submodules.

    Expected:
        All nested submodules are imported.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
                # Setup mocks
                mock_sys.modules = {}
                mock_module = mock.MagicMock()
                mock_module.__path__ = ["/path/to/package"]
                mock_module.__name__ = "test.package"
                mock_sys.modules["test.package"] = mock_module

                mock_importlib.import_module.return_value = mock_module

                # Mock pkgutil.iter_modules to return nested submodules
                mock_pkgutil.iter_modules.return_value = [
                    ("", "submodule1", False),
                    ("", "nested.submodule", False),
                    ("", "deeply.nested.submodule", False),
                ]

                # Call the function
                load_plugins_from("test.package")

                # Verify that importlib.import_module was called for the package and all submodules
                expected_calls = [
                    mock.call("submodule1"),
                    mock.call("nested.submodule"),
                    mock.call("deeply.nested.submodule"),
                ]
                mock_importlib.import_module.assert_has_calls(expected_calls)


def test_load_plugins_from_already_imported_package():
    """
    Scenario:
        Load plugins from a package that's already in sys.modules.

    Expected:
        Package is not re-imported, but submodules are still loaded.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
                # Setup mocks - package already in sys.modules
                mock_module = mock.MagicMock()
                mock_module.__path__ = ["/path/to/package"]
                mock_module.__name__ = "test.package"
                mock_sys.modules = {"test.package": mock_module}

                # Mock pkgutil.iter_modules to return some submodules
                mock_pkgutil.iter_modules.return_value = [("", "submodule1", False)]

                # Call the function
                load_plugins_from("test.package")

                # Verify that importlib.import_module was called for submodules only
                # (since the package is already in sys.modules)
                expected_calls = [mock.call("submodule1")]
                mock_importlib.import_module.assert_has_calls(expected_calls)

                # Verify that pkgutil.iter_modules was called
                mock_pkgutil.iter_modules.assert_called_with(
                    ["/path/to/package"], "test.package."
                )


def test_load_plugins_from_nonexistent_package():
    """
    Scenario:
        Load plugins from a package that doesn't exist.

    Expected:
        ImportError is raised when trying to import the package.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
            # Setup mocks
            mock_sys.modules = {}
            mock_importlib.import_module.side_effect = ImportError(
                "No module named 'nonexistent'"
            )

            # Call the function and expect ImportError
            with pytest.raises(ImportError, match="No module named 'nonexistent'"):
                load_plugins_from("nonexistent.package")


def test_load_plugins_from_package_with_import_errors():
    """
    Scenario:
        Load plugins from a package where some submodules fail to import.

    Expected:
        ImportError is raised when trying to import failing submodules.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
                # Setup mocks
                mock_sys.modules = {}
                mock_module = mock.MagicMock()
                mock_module.__path__ = ["/path/to/package"]
                mock_module.__name__ = "test.package"
                mock_sys.modules["test.package"] = mock_module

                # Mock importlib.import_module to succeed for package but fail for submodule
                def side_effect(module_name):
                    if module_name == "test.package":
                        return mock_module
                    elif module_name == "broken":
                        raise ImportError("Cannot import broken module")
                    else:
                        return mock.MagicMock()

                mock_importlib.import_module.side_effect = side_effect

                # Mock pkgutil.iter_modules to return a broken submodule
                mock_pkgutil.iter_modules.return_value = [
                    ("", "working", False),
                    ("", "broken", False),
                ]

                # Call the function and expect ImportError
                with pytest.raises(ImportError, match="Cannot import broken module"):
                    load_plugins_from("test.package")


# ---------------------------
# Integration tests
# ---------------------------


def test_load_plugins_from_real_package():
    """
    Scenario:
        Load plugins from a real package (using tidycode.plugins.config).

    Expected:
        Real package submodules are loaded successfully.
    """
    # This test uses a real package to verify the function works
    # We'll use tidycode.plugins.config which we know exists

    # Clear any existing imports to ensure clean state
    modules_to_remove = [
        name
        for name in sys.modules.keys()
        if name.startswith("tidycode.plugins.config")
    ]
    for module_name in modules_to_remove:
        del sys.modules[module_name]

    # Call the function
    load_plugins_from("tidycode.plugins.config")

    # Verify that the package and its submodules are now in sys.modules
    assert "tidycode.plugins.config" in sys.modules
    # Note: We can't assert specific submodules as they might vary


def test_load_plugins_from_module_type():
    """
    Scenario:
        Test that the function accepts both string and ModuleType.

    Expected:
        Function works with both string and ModuleType parameters.
    """
    # Test with string
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
                mock_sys.modules = {}
                mock_module = mock.MagicMock()
                mock_module.__path__ = ["/path/to/package"]
                mock_module.__name__ = "test.package"
                mock_sys.modules["test.package"] = mock_module
                mock_importlib.import_module.return_value = mock_module
                mock_pkgutil.iter_modules.return_value = []

                load_plugins_from("test.package")
                # When there are no submodules, package is not imported (already in sys.modules)
                mock_importlib.import_module.assert_not_called()

    # Test with ModuleType
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.pkgutil") as mock_pkgutil:
            mock_module = mock.MagicMock()
            mock_module.__path__ = ["/path/to/package"]
            mock_module.__name__ = "test.package"
            mock_pkgutil.iter_modules.return_value = []

            load_plugins_from(mock_module)
            mock_importlib.import_module.assert_not_called()


def test_load_plugins_from_package_without_path():
    """
    Scenario:
        Load plugins from a package that doesn't have __path__ attribute.

    Expected:
        AttributeError is raised when trying to access __path__.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
            # Setup mocks
            mock_sys.modules = {}
            mock_module = mock.MagicMock()
            # Remove __path__ attribute
            del mock_module.__path__
            mock_module.__name__ = "test.package"
            mock_sys.modules["test.package"] = mock_module
            mock_importlib.import_module.return_value = mock_module

            # Call the function and expect AttributeError
            with pytest.raises(AttributeError):
                load_plugins_from("test.package")


def test_load_plugins_from_package_without_name():
    """
    Scenario:
        Load plugins from a package that doesn't have __name__ attribute.

    Expected:
        AttributeError is raised when trying to access __name__.
    """
    with mock.patch("tidycode.plugins.loader.importlib") as mock_importlib:
        with mock.patch("tidycode.plugins.loader.sys") as mock_sys:
            # Setup mocks
            mock_sys.modules = {}
            mock_module = mock.MagicMock()
            mock_module.__path__ = ["/path/to/package"]
            # Remove __name__ attribute
            del mock_module.__name__
            mock_sys.modules["test.package"] = mock_module
            mock_importlib.import_module.return_value = mock_module

            # Call the function and expect AttributeError
            with pytest.raises(AttributeError):
                load_plugins_from("test.package")


def test_load_plugins_from_import_consistency():
    """
    Scenario:
        Test that load_plugins_from can be imported consistently.

    Expected:
        Function is properly importable.
    """
    # Test direct import
    # Test import from plugins module
    from tidycode.plugins import load_plugins_from as module_load_plugins_from
    from tidycode.plugins.loader import load_plugins_from as direct_load_plugins_from

    # Test that they are the same
    assert direct_load_plugins_from is module_load_plugins_from
    assert direct_load_plugins_from is load_plugins_from

    # Test that it's callable
    assert callable(load_plugins_from)
