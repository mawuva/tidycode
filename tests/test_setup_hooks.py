"""
Test run_hooks.py
"""

import yaml
from tidycode.core.bootstrap import setup_hooks, setup_hooks_minimal
from tidycode.utils import HOOKS

def yaml_dump(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False)

def yaml_load(text: str) -> dict:
    return yaml.safe_load(text)

def test_run_hooks_setup_remove_and_add(
    tmp_path,
    orig_config_with_hooks,
):
    config_path = tmp_path / ".pre-commit-config.yaml"

    # Write initial config file with hooks
    config_path.write_text(
        yaml_dump(orig_config_with_hooks)
    )

    removed = ["linting"]
    added = ["format_isort"]

    # Simulate user interaction with predefined return values
    def fake_ask_checkbox(msg, choices):
        if "REMOVE" in msg:
            return removed
        elif "ADD" in msg:
            return added
        elif "autoupdate" in msg:
            return ["yes"]
        return []

    commands = []

    def fake_run_command(cmd):
        commands.append(cmd)

    setup_hooks(
        ask_checkbox_fn=fake_ask_checkbox,
        run_command_fn=fake_run_command,
        config_path=config_path,
    )

    new_config = yaml_load(config_path.read_text())
    # Check that "linting" has been removed and "format_isort" has been added
    all_repos = [r["repo"] for r in new_config["repos"]]
    assert HOOKS["linting"]["yaml"]["repo"] not in all_repos
    assert HOOKS["format_isort"]["yaml"]["repo"] in all_repos
    assert ["pre-commit", "autoupdate"] in commands

def test_run_hooks_setup_minimal(tmp_path):
    config_path = tmp_path / ".pre-commit-config.yaml"
    commands = []

    def fake_run(cmd):
        commands.append(cmd)

    setup_hooks_minimal(
        config_path=config_path,
        run_command_fn=fake_run,
    )

    content = config_path.read_text()
    assert "repos" in yaml_load(content)
    assert ["pre-commit", "autoupdate"] in commands


