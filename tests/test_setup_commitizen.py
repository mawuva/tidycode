from tidycode.core.bootstrap import setup_commitizen


def test_run_commitizen_adds_config(tmp_path):
    file = tmp_path / "pyproject.toml"
    file.write_text("[tool.poetry]\nname = \"test\"\n")

    result = setup_commitizen(file)

    content = file.read_text()
    assert result is True
    assert "[tool.commitizen]" in content
    assert "cz_conventional_commits" in content


def test_run_commitizen_skips_if_already_present(tmp_path):
    file = tmp_path / "pyproject.toml"
    file.write_text("[tool.commitizen]\nname = \"already\"\n")

    result = setup_commitizen(file)

    content = file.read_text()
    assert result is False
    assert "already" in content


def test_run_commitizen_returns_false_if_file_missing(tmp_path):
    file = tmp_path / "nonexistent.toml"

    result = setup_commitizen(file)

    assert result is False
