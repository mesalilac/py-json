from dataclasses import dataclass
from .lexer import TokenPosition

type JsonValueTypes = str | int | float | bool | None | JsonData
type JsonData = dict[str, JsonValueTypes] | list[JsonValueTypes]


class ParserError(Exception):
    def __init__(self, message: str, position: TokenPosition, line: str) -> None:
        self.message = message
        self.position = position
        self.line = line
        super().__init__(f"{position.line}:{position.column} {self.message}")


@dataclass
class Parser:
    def parse(self) -> JsonData:
        raise NotImplementedError
