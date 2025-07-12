import pytest
from pathlib import Path
from tidycode.utils import inject_tool_config_in_file, load_toml_file, TOOLS_METADATA


@pytest.fixture
def black_config():
    return TOOLS_METADATA["black"]["pyproject_config"]


def test_inject_black_config(tmp_path, black_config):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.poetry]\nname = 'demo'\n")

    inject_tool_config_in_file(
        toml_file_path=pyproject,
        tool_name="black",
        config=black_config,
    )

    data = load_toml_file(pyproject)
    assert "black" in data["tool"]
    assert data["tool"]["black"]["line-length"] == 88


def test_dry_run_does_not_modify_file(tmp_path, black_config, capsys):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.poetry]\nname = 'demo'\n")

    inject_tool_config_in_file(
        toml_file_path=pyproject,
        tool_name="black",
        config=black_config,
        dry_run=True,
    )

    captured = capsys.readouterr()
    assert "line-length" in captured.out
    assert "injected" not in captured.out

    data = load_toml_file(pyproject)
    assert "black" not in data.get("tool", {})


def test_error_if_already_exists_and_not_merge(tmp_path, black_config):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        "[tool.poetry]\nname = 'demo'\n[tool.black]\nline-length = 80\n"
    )

    with pytest.raises(ValueError) as exc:
        inject_tool_config_in_file(
            toml_file_path=pyproject,
            tool_name="black",
            config=black_config,
            update_if_exists=False,
        )

    assert "already exists" in str(exc.value)


def test_merge_config_if_exists(tmp_path, black_config):
    pyproject = tmp_path / "pyproject.toml"
    # Fichier existant avec une config partielle
    pyproject.write_text(
        "[tool.poetry]\nname = 'demo'\n[tool.black]\nline-length = 100\n"
    )

    inject_tool_config_in_file(
        toml_file_path=pyproject,
        tool_name="black",
        config=black_config,
        update_if_exists=True,
    )

    data = load_toml_file(pyproject)
    assert "black" in data["tool"]
    # Le line-length original doit rester
    assert data["tool"]["black"]["line-length"] == 100
    # Les autres valeurs de config ont été injectées
    assert data["tool"]["black"]["target-version"] == ["py38"]
    assert data["tool"]["black"]["preview"] is True


def test_invalid_config_structure_raises(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.poetry]\nname = 'demo'\n")

    # Config incorrecte sans clé "tool"
    invalid_config = {"black": {"line-length": 88}}

    with pytest.raises(ValueError, match="missing 'tool.<tool_name>'"):
        inject_tool_config_in_file(
            toml_file_path=pyproject,
            tool_name="black",
            config=invalid_config,
        )
