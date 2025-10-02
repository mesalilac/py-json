import py_json.symbols as symbols

from dataclasses import dataclass, field
from enum import Enum, auto


type TokenPositionType = tuple[int, int]
type TokenValueType = str | int | float | bool | None


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
    type: TokenType
    value: TokenValueType
    position: TokenPositionType


@dataclass
class Lexer:
    source: str
    pos: int = 0
    length: int = field(init=False)
    tokens: list[Token] = field(default_factory=list)
    line: int = 1
    column: int = 1

    def __post__init__(self):
        self.length = len(self.source)
        self.tokens = self._lex()

    @staticmethod
    def is_number(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    def advance(self, by: int = 1) -> str | None:
        for _ in range(by):
            if self.pos >= self.length:
                return None
            ch = self.source[self.pos]
            self.pos += 1
            if ch == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1

        return ch

    def push_token(self, type: TokenType, value: TokenValueType = None) -> None:
        value = value

        match type:
            case TokenType.NULL:
                value = "null"
            case TokenType.LBRACE:
                value = symbols.LBRACE
            case TokenType.RBRACE:
                value = symbols.RBRACE
            case TokenType.LBRACKET:
                value = symbols.LBRACKET
            case TokenType.RBRACKET:
                value = symbols.RBRACKET
            case TokenType.COLON:
                value = symbols.COLON
            case TokenType.COMMA:
                value = symbols.COMMA

        self.tokens.append(
            Token(type=type, value=value, position=(self.line, self.column))
        )

    def peek(self, offset: int = 0) -> str | None:
        pos: int = self.pos + offset

        return self.source[pos] if pos < self.length else None

    def _lex(self) -> list[Token]:
        raise NotImplementedError
