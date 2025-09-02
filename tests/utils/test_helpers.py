"""
TidyCode Utils Helpers Tests
"""

import os
from pathlib import Path
from unittest import mock

import pytest

from tidycode.utils.helpers import ensure_file_exists, join_dot_key, split_dot_key

# ---------------------------
# Unit tests
# ---------------------------


def test_split_dot_key_simple():
    """
    Scenario:
        Split a simple dot-separated key.

    Expected:
        Returns tuple with empty list and the key name.
    """
    result = split_dot_key("key")
    assert result == ([], "key")


def test_split_dot_key_nested():
    """
    Scenario:
        Split a nested dot-separated key.

    Expected:
        Returns tuple with path list and key name.
    """
    result = split_dot_key("section.subsection.key")
    assert result == (["section", "subsection"], "key")


def test_split_dot_key_multiple_levels():
    """
    Scenario:
        Split a deeply nested dot-separated key.

    Expected:
        Returns tuple with full path list and key name.
    """
    result = split_dot_key("a.b.c.d.e.f.key")
    assert result == (["a", "b", "c", "d", "e", "f"], "key")


def test_split_dot_key_empty_string():
    """
    Scenario:
        Split an empty string.

    Expected:
        Returns tuple with empty list and empty string.
    """
    result = split_dot_key("")
    assert result == ([], "")


def test_split_dot_key_single_dot():
    """
    Scenario:
        Split a string with only a dot.

    Expected:
        Returns tuple with list containing empty string and empty string.
    """
    result = split_dot_key(".")
    assert result == ([""], "")


def test_split_dot_key_trailing_dot():
    """
    Scenario:
        Split a string with trailing dot.

    Expected:
        Returns tuple with path list and empty string.
    """
    result = split_dot_key("section.subsection.")
    assert result == (["section", "subsection"], "")


def test_join_dot_key_empty_path():
    """
    Scenario:
        Join an empty path with a key name.

    Expected:
        Returns the key name without dots.
    """
    result = join_dot_key([], "key")
    assert result == "key"


def test_join_dot_key_single_level():
    """
    Scenario:
        Join a single-level path with a key name.

    Expected:
        Returns the path and key joined by a dot.
    """
    result = join_dot_key(["section"], "key")
    assert result == "section.key"


def test_join_dot_key_multiple_levels():
    """
    Scenario:
        Join a multi-level path with a key name.

    Expected:
        Returns the full path joined by dots.
    """
    result = join_dot_key(["a", "b", "c"], "key")
    assert result == "a.b.c.key"


def test_join_dot_key_empty_key():
    """
    Scenario:
        Join a path with an empty key name.

    Expected:
        Returns the path with trailing dot.
    """
    result = join_dot_key(["section", "subsection"], "")
    assert result == "section.subsection."


def test_join_dot_key_special_characters():
    """
    Scenario:
        Join a path with special characters in key names.

    Expected:
        Returns the path correctly joined.
    """
    result = join_dot_key(["my-section", "sub_section"], "key-name")
    assert result == "my-section.sub_section.key-name"


def test_ensure_file_exists_new_file(tmp_path):
    """
    Scenario:
        Ensure a new file exists with default content.

    Expected:
        File is created with empty content.
    """
    file_path = tmp_path / "new_file.txt"
    result = ensure_file_exists(file_path)

    assert result == file_path
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == ""


def test_ensure_file_exists_new_file_with_content(tmp_path):
    """
    Scenario:
        Ensure a new file exists with specified content.

    Expected:
        File is created with the specified content.
    """
    file_path = tmp_path / "new_file.txt"
    content = "Hello, World!"
    result = ensure_file_exists(file_path, content)

    assert result == file_path
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == content


def test_ensure_file_exists_existing_file(tmp_path):
    """
    Scenario:
        Ensure an existing file exists.

    Expected:
        File remains unchanged and path is returned.
    """
    file_path = tmp_path / "existing_file.txt"
    original_content = "Original content"
    file_path.write_text(original_content, encoding="utf-8")

    result = ensure_file_exists(file_path, "New content")

    assert result == file_path
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == original_content


def test_ensure_file_exists_string_path(tmp_path):
    """
    Scenario:
        Ensure a file exists using string path.

    Expected:
        File is created and Path object is returned.
    """
    file_path = str(tmp_path / "string_path.txt")
    result = ensure_file_exists(file_path, "String path content")

    assert isinstance(result, Path)
    assert result.exists()
    assert result.read_text(encoding="utf-8") == "String path content"


def test_ensure_file_exists_nested_directories(tmp_path):
    """
    Scenario:
        Ensure a file exists in nested directories.

    Expected:
        Directories are created and file is created.
    """
    file_path = tmp_path / "nested" / "deep" / "file.txt"
    result = ensure_file_exists(file_path, "Nested content")

    assert result == file_path
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "Nested content"


def test_ensure_file_exists_mkdir_error(tmp_path):
    """
    Scenario:
        Mock mkdir to raise an error when creating parent directories.

    Expected:
        Error is propagated.
    """
    file_path = tmp_path / "subdir" / "file.txt"

    with mock.patch(
        "pathlib.Path.mkdir", side_effect=PermissionError("Permission denied")
    ):
        with pytest.raises(PermissionError) as exc_info:
            ensure_file_exists(file_path, "content")
        assert "Permission denied" in str(exc_info.value)


def test_ensure_file_exists_write_error(tmp_path):
    """
    Scenario:
        Mock write_text to raise an error when writing file content.

    Expected:
        Error is propagated.
    """
    file_path = tmp_path / "file.txt"

    with mock.patch("pathlib.Path.write_text", side_effect=OSError("Write failed")):
        with pytest.raises(OSError) as exc_info:
            ensure_file_exists(file_path, "content")
        assert "Write failed" in str(exc_info.value)


# ---------------------------
# Integration tests
# ---------------------------


def test_split_and_join_dot_key_roundtrip():
    """
    Scenario:
        Split a dot key and then join it back.

    Expected:
        The result matches the original key.
    """
    original_key = "section.subsection.key"
    path, key_name = split_dot_key(original_key)
    result = join_dot_key(path, key_name)

    assert result == original_key


def test_split_and_join_dot_key_complex():
    """
    Scenario:
        Test split and join with complex nested keys.

    Expected:
        The result matches the original key.
    """
    original_key = "a.b.c.d.e.f.g.h.i.j.k"
    path, key_name = split_dot_key(original_key)
    result = join_dot_key(path, key_name)

    assert result == original_key


def test_ensure_file_exists_with_unicode_content(tmp_path):
    """
    Scenario:
        Ensure a file exists with unicode content.

    Expected:
        File is created with correct unicode content.
    """
    file_path = tmp_path / "unicode_file.txt"
    unicode_content = "Hello, 世界! 🌍 ñöç"
    result = ensure_file_exists(file_path, unicode_content)

    assert result == file_path
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == unicode_content


def test_ensure_file_exists_multiple_files(tmp_path):
    """
    Scenario:
        Ensure multiple files exist in the same directory.

    Expected:
        All files are created with correct content.
    """
    files = [
        (tmp_path / "file1.txt", "Content 1"),
        (tmp_path / "file2.txt", "Content 2"),
        (tmp_path / "file3.txt", "Content 3"),
    ]

    for file_path, content in files:
        result = ensure_file_exists(file_path, content)
        assert result == file_path
        assert file_path.exists()
        assert file_path.read_text(encoding="utf-8") == content


def test_ensure_file_exists_relative_paths(tmp_path):
    """
    Scenario:
        Test ensure_file_exists with relative paths.

    Expected:
        Files are created correctly with relative paths.
    """
    # Change to tmp_path to test relative paths
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)

        # Test relative path
        rel_path = Path("relative_file.txt")
        result = ensure_file_exists(rel_path, "Relative content")

        assert result == rel_path
        assert rel_path.exists()
        assert rel_path.read_text(encoding="utf-8") == "Relative content"

    finally:
        os.chdir(original_cwd)
