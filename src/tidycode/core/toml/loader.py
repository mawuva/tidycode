"""
TOML file loader.
"""

from pathlib import Path
from typing import Dict, Union

from tomlkit import TOMLDocument
from tomlkit import dumps as toml_dumps
from tomlkit import parse as toml_parse


def load_toml_file(file_path: Union[str, Path]) -> TOMLDocument:
    """
    Load a TOML file and parse it into a TOMLDocument.

    Args:
        file_path (Union[str, Path]): Path to the TOML file.

    Returns:
        TOMLDocument: Parsed TOML content.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If there is an error reading or parsing the file.
    """
    file_path = Path(file_path)

    try:
        with file_path.open("r", encoding="utf-8") as f:
            return toml_parse(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file: {file_path}, {e}")


def save_toml_file(
    file_path: Union[str, Path], data: Union[Dict, TOMLDocument]
) -> None:
    """
    Save a TOML file ensuring proper directory creation and formatting.
    Adds a double newline at the end of the file.

    Args:
        file_path (Union[str, Path]): Path to write the TOML file.
        data (Union[Dict, TOMLDocument]): TOML content to save.

    Raises:
        PermissionError: If the file cannot be written due to permissions.
        Exception: If there is an error during writing.
    """
    file_path = Path(file_path)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        text = toml_dumps(data)

        if not text.endswith("\n"):
            text += "\n"
        if not text.endswith("\n\n"):
            text += "\n"

        with file_path.open("w", encoding="utf-8") as f:
            f.write(text)

    except PermissionError:
        raise PermissionError(
            f"Impossible to write file: {file_path}. Check permissions"
        )
    except Exception as e:
        raise Exception(f"Error writing file: {file_path}, {e}")
