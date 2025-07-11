"""
Conftest for tests
"""

import pytest
from tidycode.utils.hook_definitions import HOOKS

@pytest.fixture
def temp_config_file(tmp_path):
    return tmp_path / ".pre-commit-config.yaml"

@pytest.fixture
def orig_config():
    return {"repos": [{"repo": "https://repo"}]}

@pytest.fixture
def orig_config_with_hooks(orig_config):
    orig_config["repos"] += [
        HOOKS["linting"]["yaml"],
        HOOKS["format_black"]["yaml"]
    ]
    return orig_config