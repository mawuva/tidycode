"""
TidyCode Core PyProject Types Tests
"""

from tidycode.core.pyproject.types import (
    GlobalActions,
    KeyActions,
    Mode,
    OverwriteChoice,
    PrintSectionSummaryMode,
    PyProjectHiddenSections,
    PyProjectHiddenSubsections,
    RemoveSectionChoices,
    SensitiveKeys,
    SensitiveKeywords,
)


def test_overwrite_choice_enum():
    """
    Scenario:
        Test the OverwriteChoice enum values.

    Expected:
        All expected choices are available.
    """
    assert OverwriteChoice.OVERWRITE == "overwrite"
    assert OverwriteChoice.ADD_KEYS == "add keys"
    assert OverwriteChoice.ADD_SUBSECTION == "add subsection"
    assert OverwriteChoice.CANCEL == "cancel"

    # Test to_list method
    choices = OverwriteChoice.to_list()
    assert len(choices) == 4
    assert "overwrite" in choices
    assert "add keys" in choices
    assert "add subsection" in choices
    assert "cancel" in choices


def test_global_actions_enum():
    """
    Scenario:
        Test the GlobalActions enum values.

    Expected:
        All expected actions are available.
    """
    assert GlobalActions.ADD_KEYS == "add keys"
    assert GlobalActions.ADD_SUBSECTION == "add subsection"
    assert GlobalActions.EDIT == "edit"
    assert GlobalActions.REMOVE == "remove"
    assert GlobalActions.EXIT == "exit"

    # Test to_list method
    actions = GlobalActions.to_list()
    assert len(actions) == 5
    assert "add keys" in actions
    assert "add subsection" in actions
    assert "edit" in actions
    assert "remove" in actions
    assert "exit" in actions


def test_mode_enum():
    """
    Scenario:
        Test the Mode enum values.

    Expected:
        All expected modes are available.
    """
    assert Mode.ADD == "add"
    assert Mode.EDIT == "edit"
    assert Mode.REMOVE == "remove"
    assert Mode.FULL == "full"

    # Test to_list method
    modes = Mode.to_list()
    assert len(modes) == 4
    assert "add" in modes
    assert "edit" in modes
    assert "remove" in modes
    assert "full" in modes


def test_key_actions_enum():
    """
    Scenario:
        Test the KeyActions enum values.

    Expected:
        All expected key actions are available.
    """
    assert KeyActions.EDIT == "edit"
    assert KeyActions.REMOVE == "remove"
    assert KeyActions.SKIP == "skip"

    # Test to_list method
    actions = KeyActions.to_list()
    assert len(actions) == 3
    assert "edit" in actions
    assert "remove" in actions
    assert "skip" in actions


def test_pyproject_hidden_sections_enum():
    """
    Scenario:
        Test the PyProjectHiddenSections enum values.

    Expected:
        All expected hidden sections are available.
    """
    assert PyProjectHiddenSections.PROJECT == "project"
    assert PyProjectHiddenSections.POETRY == "tool.poetry"
    assert PyProjectHiddenSections.BUILD_SYSTEM == "build-system"

    # Test to_list method
    sections = PyProjectHiddenSections.to_list()
    assert len(sections) == 3
    assert "project" in sections
    assert "tool.poetry" in sections
    assert "build-system" in sections


def test_pyproject_hidden_subsections_enum():
    """
    Scenario:
        Test the PyProjectHiddenSubsections enum values.

    Expected:
        All expected hidden subsections are available.
    """
    assert PyProjectHiddenSubsections.POETRY == "poetry"

    # Test to_list method
    subsections = PyProjectHiddenSubsections.to_list()
    assert len(subsections) == 1
    assert "poetry" in subsections


def test_sensitive_keys_enum():
    """
    Scenario:
        Test the SensitiveKeys enum values.

    Expected:
        All expected sensitive keys are available.
    """
    assert SensitiveKeys.API_KEY == "api_key"
    assert SensitiveKeys.TOKEN == "token"
    assert SensitiveKeys.PASSWORD == "password"
    assert SensitiveKeys.SECRET == "secret"
    assert SensitiveKeys.BLACK == "black"
    assert SensitiveKeys.POETRY == "poetry"

    # Test to_list method
    keys = SensitiveKeys.to_list()
    assert len(keys) == 6
    assert "api_key" in keys
    assert "token" in keys
    assert "password" in keys
    assert "secret" in keys
    assert "black" in keys
    assert "poetry" in keys


def test_sensitive_keywords_enum():
    """
    Scenario:
        Test the SensitiveKeywords enum values.

    Expected:
        All expected sensitive keywords are available.
    """
    assert SensitiveKeywords.POETRY == "poetry"
    assert SensitiveKeywords.BLACK == "black"
    assert SensitiveKeywords.RUFF == "ruff"
    assert SensitiveKeywords.ISORT == "isort"

    # Test to_list method
    keywords = SensitiveKeywords.to_list()
    assert len(keywords) == 4
    assert "poetry" in keywords
    assert "black" in keywords
    assert "ruff" in keywords
    assert "isort" in keywords


def test_print_section_summary_mode_enum():
    """
    Scenario:
        Test the PrintSectionSummaryMode enum values.

    Expected:
        All expected print modes are available.
    """
    assert PrintSectionSummaryMode.TREE == "tree"
    assert PrintSectionSummaryMode.LIST == "list"
    assert PrintSectionSummaryMode.TABLE == "table"
    assert PrintSectionSummaryMode.JSON == "json"

    # Test to_list method
    modes = PrintSectionSummaryMode.to_list()
    assert len(modes) == 4
    assert "tree" in modes
    assert "list" in modes
    assert "table" in modes
    assert "json" in modes


def test_remove_section_choices_enum():
    """
    Scenario:
        Test the RemoveSectionChoices enum values.

    Expected:
        All expected remove choices are available.
    """
    assert RemoveSectionChoices.ENTIRE_SECTION == "entire section"
    assert RemoveSectionChoices.KEYS_ONLY == "keys only"
    assert RemoveSectionChoices.EXIT == "exit"

    # Test to_list method
    choices = RemoveSectionChoices.to_list()
    assert len(choices) == 3
    assert "entire section" in choices
    assert "keys only" in choices
    assert "exit" in choices


def test_enum_inheritance():
    """
    Scenario:
        Test that all enums inherit from BaseEnum.

    Expected:
        All enums have the expected methods from BaseEnum.
    """
    enums = [
        OverwriteChoice,
        GlobalActions,
        Mode,
        KeyActions,
        PyProjectHiddenSections,
        PyProjectHiddenSubsections,
        SensitiveKeys,
        SensitiveKeywords,
        PrintSectionSummaryMode,
        RemoveSectionChoices,
    ]

    for enum_class in enums:
        # Test that to_list method exists
        assert hasattr(enum_class, "to_list")
        assert callable(enum_class.to_list)

        # Test that from_value method exists
        assert hasattr(enum_class, "from_value")
        assert callable(enum_class.from_value)
