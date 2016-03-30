"""
Converts text to tokens to be consumed by the parser
"""
from __future__ import unicode_literals
from pygments import lex
from pygments.lexers.matlab import MatlabLexer
from pygments.token import (
    Text,
    Punctuation,
    Operator,
    Literal,
)


class Token(object):
    END_OF_LINE = 'END_OF_LINE'
    LEFT_PARENTHESIS = 'LEFT_PARENTHESIS'
    RIGHT_PARENTHESIS = 'RIGHT_PARENTHESIS'
    LEFT_SQUARE_BRACKET = 'LEFT_SQUARE_BRACKET'
    RIGHT_SQUARE_BRACKET = 'RIGHT_SQUARE_BRACKET'
    COMMA = 'COMMA'
    SEMI_COLON = 'SEMI_COLON'
    ADD_OPERATOR = 'ADD_OPERATOR'
    SUBTRACT_OPERATOR = 'SUBTRACT_OPERATOR'
    MULTIPLY_OPERATOR = 'MULTIPLY_OPERATOR'
    DIVIDE_OPERATOR = 'DIVIDE_OPERATOR'
    INTEGER_LITERAL = Literal.Number.Integer


class Lexer(object):
    token_map = {
        (Text, u'\n'): Token.END_OF_LINE,
        (Punctuation, u','): Token.COMMA,
        (Punctuation, u';'): Token.SEMI_COLON,
        (Punctuation, u'['): Token.LEFT_SQUARE_BRACKET,
        (Punctuation, u']'): Token.RIGHT_SQUARE_BRACKET
    }

    @classmethod
    def lex(cls, line):
        tokens = lex(line, MatlabLexer())
        # remove all whitespace except new line at the end
        tokens = filter(
            lambda _token: _token[0] != Text or _token[1] == u'\n',
            tokens
        )
        return [
            (cls.token_map.get(token, token[0]), token[1])
            for token in tokens
        ]
