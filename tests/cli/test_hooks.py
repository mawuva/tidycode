import os
import pytest
from typer.testing import CliRunner
from tidycode.cli.main import app

runner = CliRunner()

@pytest.mark.skipif(os.name == "nt", reason="CliRunner + questionary fails on Windows")
def test_hooks_interactive_no_crash(tmp_path):
    result = runner.invoke(app, ["hooks", "setup", "--config-path", str(tmp_path / "x.yaml")], input="\n\n\n")
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


