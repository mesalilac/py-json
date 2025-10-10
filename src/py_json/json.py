from dataclasses import dataclass
from typing import TYPE_CHECKING, TextIO

if TYPE_CHECKING:
    from .parser import JsonData


@dataclass
class Json:
    @staticmethod
    def load(fp: TextIO) -> JsonData:
        """Load json from a file."""
        raise NotImplementedError

    @staticmethod
    def loads(s: str) -> JsonData:
        """Load json from a string."""
        raise NotImplementedError

    def dump(obj: JsonData, fp: TextIO) -> None:
        """Serialize into json and write to file."""
        raise NotImplementedError

    def dumps(obj: JsonData) -> str:
        """Serialize into json and return as a string."""
        raise NotImplementedError
