"""
Base Enum with common helper methods for CLI prompts.
"""

from enum import Enum
from typing import List, Type, TypeVar

T = TypeVar("T", bound="BaseEnum")


class BaseEnum(str, Enum):
    """Base Enum with common helper methods for CLI prompts."""

    @classmethod
    def to_list(cls) -> List[str]:
        """Return a list of all enum values."""
        return [item.value for item in cls]

    @classmethod
    def has_value(cls, value: str) -> bool:
        """Check if a value exists in the enum."""
        return value in cls.to_list()

    @classmethod
    def from_value(cls: Type[T], value: str) -> T:
        """Return the Enum member corresponding to the value."""
        for item in cls:
            if item.value == value:
                return item
        raise ValueError(f"{value} is not a valid {cls.__name__}")
