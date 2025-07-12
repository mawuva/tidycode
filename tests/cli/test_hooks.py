import os
import pytest
from typer.testing import CliRunner
from tidycode.cli.main import app
from tidycode.utils import HOOKS, yaml_dump, yaml_load, get_iter_hook_with_yaml

runner = CliRunner()


@pytest.fixture
def patch_run(monkeypatch):
    called = []

    def fake(cmd):
        called.append(cmd)

    monkeypatch.setattr("tidycode.cli.commands.hooks.run_command", fake)
    return called


@pytest.mark.skipif(os.name == "nt", reason="CliRunner + questionary fails on Windows")
def test_hooks_interactive_no_crash(tmp_path, patch_run):
    result = runner.invoke(
        app,
        ["hooks", "setup", "--config-path", str(tmp_path / "x.yaml")],
        input="\n\n\n",
    )
    assert result.exit_code == 0


def test_hooks_setup_minimal_command(tmp_path):
    from tidycode.core.bootstrap.setup_hooks import setup_hooks_minimal

    config_path = tmp_path / ".pre-commit-config.yaml"
    commands = []

    def fake_run(cmd):
        commands.append(cmd)

    def fake_confirm(msg):
        return False

    setup_hooks_minimal(
        config_path=config_path,
        run_command_fn=fake_run,
        ask_confirm_fn=fake_confirm,
    )

    assert config_path.exists()
    assert len(commands) == 0


def test_install_adds_hooks_and_calls_pre_commit_install(tmp_path, patch_run):
    config = tmp_path / "conf.yaml"
    config.write_text("")
    result = runner.invoke(app, ["hooks", "install"])
    assert result.exit_code == 0
    assert ["pre-commit", "install"] in patch_run


def test_uninstall_calls_pre_commit_uninstall(patch_run):
    result = runner.invoke(app, ["hooks", "uninstall"])
    assert result.exit_code == 0
    assert ["pre-commit", "uninstall"] in patch_run


def test_update_calls_pre_commit_autoupdate(patch_run):
    result = runner.invoke(app, ["hooks", "update"])
    assert result.exit_code == 0
    assert ["pre-commit", "autoupdate"] in patch_run


def test_check_calls_pre_commit_run_all_files(patch_run):
    result = runner.invoke(app, ["hooks", "check"])
    assert result.exit_code == 0
    assert ["pre-commit", "run", "--all-files"] in patch_run


def test_list_available():
    result = runner.invoke(app, ["hooks", "list-available"])
    assert result.exit_code == 0
    for key in HOOKS:
        assert key in result.output


def test_list_installed_with_hooks(tmp_path):
    config_path = tmp_path / ".pre-commit-config.yaml"
    # simulate config with two hooks
    config_data = {
        "repos": [HOOKS[k]["yaml"] for k in list(HOOKS)[:2] if "yaml" in HOOKS[k]]
    }
    config_path.write_text(yaml_dump(config_data))
    result = runner.invoke(
        app, ["hooks", "list-installed", "--config-path", str(config_path)]
    )
    assert result.exit_code == 0
    for k in list(HOOKS)[:2]:
        if "yaml" in HOOKS[k]:
            assert k in result.output


def test_clean_removes_hooks(tmp_path):
    config_path = tmp_path / ".pre-commit-config.yaml"
    initial_hooks = [HOOKS[k]["yaml"] for k in list(HOOKS)[:2] if "yaml" in HOOKS[k]]
    config_path.write_text(yaml_dump({"repos": initial_hooks}))
    result = runner.invoke(app, ["hooks", "clean", "--config-path", str(config_path)])
    assert result.exit_code == 0
    content = yaml_load(config_path.read_text())
    assert content.get("repos", []) == []


def test_sync_installs_hooks_when_none(tmp_path, patch_run):
    config_path = tmp_path / ".pre-commit-config.yaml"
    config_path.write_text("")
    result = runner.invoke(app, ["hooks", "sync", "--config-path", str(config_path)])
    assert result.exit_code == 0
    assert ["pre-commit", "install"] in patch_run


def test_sync_updates_hooks_when_already_installed(tmp_path, patch_run):
    config_path = tmp_path / ".pre-commit-config.yaml"
    # Add one hook manually
    hook_with_yaml = get_iter_hook_with_yaml()
    config_path.write_text(yaml_dump({"repos": [HOOKS[hook_with_yaml]["yaml"]]}))
    result = runner.invoke(app, ["hooks", "sync", "--config-path", str(config_path)])
    assert result.exit_code == 0
    assert ["pre-commit", "autoupdate"] in patch_run


def test_reset_removes_hooks_and_uninstalls(tmp_path, patch_run):
    config_path = tmp_path / ".pre-commit-config.yaml"
    # Add hooks
    hook_with_yaml = get_iter_hook_with_yaml()
    config_path.write_text(yaml_dump({"repos": [HOOKS[hook_with_yaml]["yaml"]]}))
    result = runner.invoke(app, ["hooks", "reset", "--config-path", str(config_path)])
    assert result.exit_code == 0
    config = yaml_load(config_path.read_text())
    assert config.get("repos", []) == []
    assert ["pre-commit", "uninstall"] in patch_run
