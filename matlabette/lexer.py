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
    Name,
    Token as PygmentsToken
)


class Token(object):
    END_OF_LINE = 'END_OF_LINE'
    LEFT_PARENTHESIS = 'LEFT_PARENTHESIS'
    RIGHT_PARENTHESIS = 'RIGHT_PARENTHESIS'
    LEFT_SQUARE_BRACKET = 'LEFT_SQUARE_BRACKET'
    RIGHT_SQUARE_BRACKET = 'RIGHT_SQUARE_BRACKET'
    COMMA = 'COMMA'
    SEMI_COLON = 'SEMI_COLON'
    ASSIGN_OPERATOR = 'ASSIGN_OPERATOR'
    ADD_OPERATOR = 'ADD_OPERATOR'
    SUBTRACT_OPERATOR = 'SUBTRACT_OPERATOR'
    MULTIPLY_OPERATOR = 'MULTIPLY_OPERATOR'
    DIVIDE_OPERATOR = 'DIVIDE_OPERATOR'
    ELEM_ADD_OPERATOR = 'ELEM_ADD_OPERATOR'
    ELEM_SUBTRACT_OPERATOR = 'ELEM_SUBTRACT_OPERATOR'
    ELEM_MULTIPLY_OPERATOR = 'ELEM_MULTIPLY_OPERATOR'
    ELEM_DIVIDE_OPERATOR = 'ELEM_DIVIDE_OPERATOR'
    TRANSPOSE_OPERATOR = 'TRANSPOSE_OPERATOR'
    INTEGER_LITERAL = Literal.Number.Integer
    FLOAT_LITERAL = Literal.Number.Float
    VARIABLE_NAME = Name
    BUILTIN_NAME = PygmentsToken.Name.Builtin


class Lexer(object):
    token_map = {
        (Text, u'\n'): Token.END_OF_LINE,
        (Punctuation, u','): Token.COMMA,
        (Punctuation, u';'): Token.SEMI_COLON,
        (Punctuation, u'['): Token.LEFT_SQUARE_BRACKET,
        (Punctuation, u']'): Token.RIGHT_SQUARE_BRACKET,
        (Punctuation, u'('): Token.LEFT_PARENTHESIS,
        (Punctuation, u')'): Token.RIGHT_PARENTHESIS,
        (Punctuation, u'='): Token.ASSIGN_OPERATOR,
        (Operator, u'+'): Token.ADD_OPERATOR,
        (Operator, u'*'): Token.MULTIPLY_OPERATOR,
        (Operator, u'-'): Token.SUBTRACT_OPERATOR,
        (Operator, u'/'): Token.DIVIDE_OPERATOR,
        (Operator, u'.+'): Token.ELEM_ADD_OPERATOR,
        (Operator, u'.*'): Token.ELEM_MULTIPLY_OPERATOR,
        (Operator, u'.-'): Token.ELEM_SUBTRACT_OPERATOR,
        (Operator, u'./'): Token.ELEM_DIVIDE_OPERATOR,
        (Operator, u'\''): Token.TRANSPOSE_OPERATOR,
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
