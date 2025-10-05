from py_json.lexer import Lexer
from py_json.lexer import TokenType as Type


def collect_types(text: str):
    return [t.type for t in Lexer(text).tokens]


def with_eof(*types: Type) -> list[Type]:
    return [*types, Type.EOF]


def test_whitespace_only():
    assert collect_types("    \n\t    ") == [Type.EOF]


def test_whitespace_between_tokens():
    text = '{    "a"    :    1    }'
    expected = with_eof(
        Type.LBRACE,
        Type.STRING,
        Type.COLON,
        Type.NUMBER,
        Type.RBRACE,
    )

    assert collect_types(text) == expected


def test_empty_string():
    assert collect_types('""') == with_eof(Type.STRING)


def test_string_with_space():
    assert collect_types('"hello world"') == with_eof(Type.STRING)


def test_string_with_escaped_quote():
    assert collect_types(r'"he said \"hi\""') == with_eof(Type.STRING)


def test_string_with_unicode_escape():
    assert collect_types(r'"\u0041"') == with_eof(Type.STRING)


def test_string_with_backslash_escape():
    assert collect_types(r'"line1\nline2"') == with_eof(Type.STRING)


def test_zero():
    assert collect_types("0") == with_eof(Type.NUMBER)


def test_negative_zero():
    assert collect_types("-0") == with_eof(Type.NUMBER)


def test_leading_zero_integer():
    assert collect_types("0123") == with_eof(Type.NUMBER)


def test_decimal_no_leading_digit():
    assert collect_types(".5") == with_eof(Type.ILLEGAL, Type.NUMBER)


def test_large_exponent():
    assert collect_types("1e+308") == with_eof(Type.NUMBER)


def test_array_with_mixed_types():
    text = '[1, "two", true, false, null]'
    expected = with_eof(
        Type.LBRACKET,
        *(Type.NUMBER, Type.COMMA),
        *(Type.STRING, Type.COMMA),
        *(Type.TRUE, Type.COMMA),
        *(Type.FALSE, Type.COMMA),
        Type.NULL,
        Type.RBRACKET,
    )

    assert collect_types(text) == expected


def test_array_nested_objects():
    text = '[{"a":1}, {"b":2}]'
    expected = with_eof(
        Type.LBRACKET,
        *(Type.LBRACE, Type.STRING, Type.COLON, Type.NUMBER, Type.RBRACE, Type.COMMA),
        *(Type.LBRACE, Type.STRING, Type.COLON, Type.NUMBER, Type.RBRACE),
        Type.RBRACKET,
    )

    assert collect_types(text) == expected


def test_object_with_array_value():
    text = '{"arr":[1,2,3]}'
    expected = with_eof(
        Type.LBRACE,
        *(Type.STRING, Type.COLON),
        Type.LBRACKET,
        *(Type.NUMBER, Type.COMMA),
        *(Type.NUMBER, Type.COMMA),
        Type.NUMBER,
        Type.RBRACKET,
        Type.RBRACE,
    )

    assert collect_types(text) == expected


def test_object_with_nested_mixed():
    text = '{"outer":{"inner":[true,false,null]}}'
    expected = with_eof(
        Type.LBRACE,
        *(Type.STRING, Type.COLON),
        Type.LBRACE,
        *(Type.STRING, Type.COLON),
        Type.LBRACKET,
        *(Type.TRUE, Type.COMMA),
        *(Type.FALSE, Type.COMMA),
        Type.NULL,
        Type.RBRACKET,
        Type.RBRACE,
        Type.RBRACE,
    )

    assert collect_types(text) == expected


def test_deeply_nested_arrays():
    text = "[[[[[42]]]]]"
    expected = with_eof(
        Type.LBRACKET,
        Type.LBRACKET,
        Type.LBRACKET,
        Type.LBRACKET,
        Type.LBRACKET,
        Type.NUMBER,
        Type.RBRACKET,
        Type.RBRACKET,
        Type.RBRACKET,
        Type.RBRACKET,
        Type.RBRACKET,
    )

    assert collect_types(text) == expected
