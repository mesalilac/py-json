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
    _source: str
    _pos: int = 0
    _length: int = field(init=False)
    tokens: list[Token] = field(default_factory=list)
    _line: int = 1
    _column: int = 1

    def __post__init__(self):
        self._length = len(self._source)
        self.tokens = self._lex()

    @staticmethod
    def _is_number(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def _is_float(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    def _advance(self, by: int = 1) -> str | None:
        for _ in range(by):
            if self._pos >= self._length:
                return None
            ch = self._source[self._pos]
            self._pos += 1
            if ch == "\n":
                self._line += 1
                self._column = 1
            else:
                self._column += 1

        return ch

    def _push_token(self, type: TokenType, value: TokenValueType = None) -> None:
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
            Token(type=type, value=value, position=(self._line, self._column))
        )

    def _peek(self, offset: int = 0) -> str | None:
        pos: int = self._pos + offset

        return self._source[pos] if pos < self._length else None

    def _lex(self) -> list[Token]:
        raise NotImplementedError
