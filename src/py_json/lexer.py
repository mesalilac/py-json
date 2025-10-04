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

    ILLEGAL = auto()
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

    def __post_init__(self):
        self._length = len(self._source)
        self._lex()

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

    def _lex(self) -> None:
        while self._pos < self._length:
            ch: str = self._source[self._pos]

            if ch == symbols.NEWLINE:
                self._advance()
            elif ch.isspace():
                self._advance()
            elif ch == symbols.COMMA:
                self._push_token(TokenType.COMMA)
                self._advance()
            elif ch == symbols.COLON:
                self._push_token(TokenType.COLON)
                self._advance()
            elif ch == symbols.LBRACKET:
                self._push_token(TokenType.LBRACKET)
                self._advance()
            elif ch == symbols.RBRACKET:
                self._push_token(TokenType.RBRACKET)
                self._advance()
            elif ch == symbols.LBRACE:
                self._push_token(TokenType.LBRACE)
                self._advance()
            elif ch == symbols.RBRACE:
                self._push_token(TokenType.RBRACE)
                self._advance()
            elif ch.isalpha():
                buffer = ""

                while self._source[self._pos].isalpha():
                    buffer += self._source[self._pos]
                    self._advance()

                if buffer.lower() == "true":
                    self._push_token(TokenType.TRUE)
                elif buffer.lower() == "false":
                    self._push_token(TokenType.FALSE)
                elif buffer.lower() == "null":
                    self._push_token(TokenType.NULL)
                else:
                    self._push_token(
                        TokenType.ILLEGAL, buffer[-1] if buffer else buffer
                    )
            elif ch.isdigit() or ch in "-.":
                buffer = ""

                while self._pos < self._length and (
                    self._source[self._pos].isdigit()
                    or self._source[self._pos].lower() in "-+._e"
                ):
                    buffer += self._source[self._pos]
                    self._advance()

                if self._is_number(buffer) and "." not in buffer:
                    self._push_token(TokenType.NUMBER, int(buffer))
                elif self._is_float(buffer):
                    self._push_token(TokenType.NUMBER, float(buffer))
                else:
                    self._push_token(
                        TokenType.ILLEGAL, buffer[-1] if buffer else buffer
                    )
            elif ch == symbols.DOUBLE_QUOTE:
                self._advance()

                buffer = ""

                while self._pos < self._length:
                    curr_ch = self._source[self._pos]

                    if curr_ch == symbols.DOUBLE_QUOTE:
                        backslashes = 0
                        i = self._pos - 1

                        while i >= 0 and self._source[i] == "\\":
                            backslashes += 1
                            i -= 1
                        if backslashes % 2 == 0:  # If even it's not escaped
                            break

                    buffer += self._source[self._pos]
                    self._advance()

                if self._source[self._pos] == symbols.DOUBLE_QUOTE:
                    self._advance()

                self._push_token(TokenType.STRING, buffer)
            else:
                self._push_token(TokenType.ILLEGAL, ch)
                self._advance()

        self._push_token(TokenType.EOF)
