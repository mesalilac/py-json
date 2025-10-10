from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from py_json.lexer import Token, TokenPositionType

type JsonValueTypes = str | int | float | bool | None | JsonData
type JsonData = dict[str, JsonValueTypes] | list[JsonValueTypes]


class ParserError(Exception):
    def __init__(self, message: str, position: TokenPositionType) -> None:
        self.message = message
        self.position = position

        super().__init__(f"{position[0]}:{position[1]} {self.message}")


@dataclass
class Parser:
    _tokens: list[Token]
    _pos: int = 0
    _length: int = field(init=False)

    def __post_init__(self) -> None:
        self._length = len(self._tokens)
        self._parse()

    def _parse(self) -> JsonData:
        """Parse list tokens and return `{}` or `[]`."""
        raise NotImplementedError
