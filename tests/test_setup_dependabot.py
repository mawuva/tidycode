"""
Test setup_dependabot.py
"""

from tidycode.core.bootstrap import setup_dependabot


def test_run_dependabot_creates_file(tmp_path):
    path = tmp_path / ".github" / "dependabot.yml"
    result = setup_dependabot(path)

    assert result is True
    assert path.exists()
    content = path.read_text()
    assert "version: 2" in content
    assert "pip" in content


def test_run_dependabot_skips_if_exists(tmp_path):
    path = tmp_path / ".github" / "dependabot.yml"
    path.parent.mkdir(parents=True)
    path.write_text("version: 2\nupdates: []")

    result = setup_dependabot(path)

    assert result is False
    assert path.read_text() == "version: 2\nupdates: []"
