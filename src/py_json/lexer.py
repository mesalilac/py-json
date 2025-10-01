from dataclasses import dataclass
from enum import Enum, auto


@dataclass
class TokenPosition:
    line: int
    column: int


class TokenType(Enum):
    # Structure
    LBRACE = auto()  # {
    RBRACE = auto()  # }
    LBRACKET = auto()  # [
    RBRACKET = auto()  # ]
    COLON = auto()  # :
    COMMA = auto()  # ,

    # Literal Value Tokens
    STRING = auto()
    NUMBER = auto()
    TRUE = auto()
    FALSE = auto()
    NULL = auto()  # JSON null

    EOF = auto()  # End of file Token


@dataclass
class Token:
    pass


@dataclass
class Lexer:
    def tokens(self) -> list[Token]:
        raise NotImplementedError
