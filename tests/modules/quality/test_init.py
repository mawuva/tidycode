"""
Tests for quality module __init__.py.
"""

from unittest import mock


class TestQualityModuleInit:
    """Test cases for quality module __init__.py."""

    def test_quality_module_imports(self):
        """
        Scenario:
            Import from quality module.

        Expected:
            All expected imports are available.
        """
        from tidycode.modules.quality import run_quality_tools

        assert run_quality_tools is not None
        assert callable(run_quality_tools)

    def test_quality_module_all_exports(self):
        """
        Scenario:
            Check __all__ exports.

        Expected:
            __all__ contains expected exports.
        """
        from tidycode.modules.quality import __all__

        expected_exports = ["run_quality_tools"]
        assert __all__ == expected_exports

    def test_quality_module_import_consistency(self):
        """
        Scenario:
            Test import consistency from different paths.

        Expected:
            Imports work consistently from different paths.
        """
        # Test direct import
        from tidycode.modules.quality import run_quality_tools as direct_import

        # Test import from orchestrator
        from tidycode.modules.quality.orchestrator import (
            run_quality_tools as orchestrator_import,
        )

        # Verify both imports are the same
        assert direct_import is orchestrator_import

    def test_quality_module_function_signatures(self):
        """
        Scenario:
            Test function signatures.

        Expected:
            Function has expected signature.
        """
        import inspect

        from tidycode.modules.quality import run_quality_tools

        # Get function signature
        sig = inspect.signature(run_quality_tools)

        # Check parameter names
        param_names = list(sig.parameters.keys())
        expected_params = [
            "tools",
            "check_only",
            "live",
            "verbose",
            "summary_display_mode",
        ]
        assert param_names == expected_params

        # Check parameter defaults
        assert sig.parameters["tools"].default is None
        assert sig.parameters["check_only"].default is False
        assert sig.parameters["live"].default is False
        assert sig.parameters["verbose"].default is True
        assert sig.parameters["summary_display_mode"].default is None

    def test_quality_module_class_attributes(self):
        """
        Scenario:
            Test module attributes.

        Expected:
            Module has expected attributes.
        """
        import tidycode.modules.quality as quality_module

        # Check __all__ attribute
        assert hasattr(quality_module, "__all__")
        assert quality_module.__all__ == ["run_quality_tools"]

        # Check docstring
        assert hasattr(quality_module, "__doc__")
        assert "Quality module." in quality_module.__doc__

    def test_quality_module_registry_instance(self):
        """
        Scenario:
            Test that the module can be imported without errors.

        Expected:
            Module imports successfully.
        """
        # This test ensures the module can be imported
        import tidycode.modules.quality

        assert tidycode.modules.quality is not None

    def test_quality_module_protocol_compliance(self):
        """
        Scenario:
            Test that imported function is callable.

        Expected:
            Function is properly callable.
        """
        from tidycode.modules.quality import run_quality_tools

        assert callable(run_quality_tools)

    def test_quality_module_decorator_functionality(self):
        """
        Scenario:
            Test that the module exports work as expected.

        Expected:
            Exports work correctly.
        """
        from tidycode.modules.quality import run_quality_tools

        # Test that the function can be called (with mocked dependencies)
        with mock.patch(
            "tidycode.modules.quality.orchestrator.load_tidycode_config"
        ) as mock_config:
            with mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from"):
                with mock.patch(
                    "tidycode.modules.quality.orchestrator.registry"
                ) as mock_registry:
                    with mock.patch(
                        "tidycode.modules.quality.orchestrator.run_multiple_commands"
                    ):
                        mock_config.return_value = {
                            "target": ".",
                            "check_only": False,
                            "tools": [],
                        }
                        mock_registry.by_category.return_value = []

                        # This should not raise an exception
                        run_quality_tools()

    def test_quality_module_loader_functionality(self):
        """
        Scenario:
            Test that the module can be loaded dynamically.

        Expected:
            Module loads correctly.
        """
        import importlib

        # Test dynamic import
        quality_module = importlib.import_module("tidycode.modules.quality")

        assert hasattr(quality_module, "run_quality_tools")
        assert callable(quality_module.run_quality_tools)

    def test_quality_module_integration(self):
        """
        Scenario:
            Test integration with the rest of the system.

        Expected:
            Module integrates correctly.
        """
        from tidycode.modules.quality import run_quality_tools

        # Test that the function exists and is callable
        assert run_quality_tools is not None
        assert callable(run_quality_tools)

        # Test that it can be imported from the parent module
        from tidycode.modules import quality

        assert hasattr(quality, "run_quality_tools")
        assert quality.run_quality_tools is run_quality_tools

    def test_quality_module_enum_values(self):
        """
        Scenario:
            Test that the module works with enum values.

        Expected:
            Module handles enum values correctly.
        """
        from tidycode.modules.quality import run_quality_tools
        from tidycode.runner import SubprocessDisplayMode

        # Test that the function can accept enum values
        with mock.patch(
            "tidycode.modules.quality.orchestrator.load_tidycode_config"
        ) as mock_config:
            with mock.patch("tidycode.modules.quality.orchestrator.load_plugins_from"):
                with mock.patch(
                    "tidycode.modules.quality.orchestrator.registry"
                ) as mock_registry:
                    with mock.patch(
                        "tidycode.modules.quality.orchestrator.run_multiple_commands"
                    ):
                        mock_config.return_value = {
                            "target": ".",
                            "check_only": False,
                            "tools": [],
                        }
                        mock_registry.by_category.return_value = []

                        # This should not raise an exception
                        run_quality_tools(
                            summary_display_mode=SubprocessDisplayMode.TABLE_FULL
                        )
