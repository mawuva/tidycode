import pytest
from tidycode.core.bootstrap import setup_commitizen
from tidycode.utils import load_toml_file


@pytest.fixture
def fake_run_command():
    calls = []

    def _fake(cmd):
        calls.append(cmd)

    return _fake, calls


def test_setup_commitizen_no_pyproject(tmp_path):
    path = tmp_path / "pyproject.toml"
    assert setup_commitizen(path) is False


def test_setup_commitizen_already_present(tmp_path):
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.commitizen]\nname = 'cz_conventional_commits'\n")
    assert setup_commitizen(path) is False


def test_setup_commitizen_injects_config(tmp_path, fake_run_command):
    path = tmp_path / "pyproject.toml"
    path.write_text("")  # empty file

    run_command_fn, calls = fake_run_command
    success = setup_commitizen(path, run_command_fn=run_command_fn)
    assert success is True

    config = load_toml_file(path)
    assert config["tool"]["commitizen"]["name"] == "cz_conventional_commits"
    assert ["cz", "init", "--name", "cz_conventional_commits", "--yes"] in calls


def test_setup_commitizen_dry_run(tmp_path, capsys):
    path = tmp_path / "pyproject.toml"
    path.write_text("")

    success = setup_commitizen(path, dry_run=True)
    assert success is True

    # Should not save to file
    content = path.read_text()
    assert "commitizen" not in content

    # Check diff was printed
    captured = capsys.readouterr()
    assert "+ [tool.commitizen]" in captured.out


def test_setup_commitizen_cz_init_failure(tmp_path):
    path = tmp_path / "pyproject.toml"
    path.write_text("")

    def _fail_command(cmd):
        raise Exception("fail cz")

    success = setup_commitizen(path, run_command_fn=_fail_command)
    assert success is True  # config was written
    content = path.read_text()
    assert "commitizen" in content


def test_setup_commitizen_adds_tool_if_missing(tmp_path, fake_run_command):
    """Make sure [tool] is created if absent"""
    path = tmp_path / "pyproject.toml"
    path.write_text("")  # no [tool] section

    run_command_fn, _ = fake_run_command
    success = setup_commitizen(path, dry_run=False, run_command_fn=run_command_fn)
    assert success is True

    config = load_toml_file(path)
    assert "tool" in config
    assert "commitizen" in config["tool"]
