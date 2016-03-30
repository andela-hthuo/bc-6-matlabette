"""
Takes a list tokens and converts them to a parse tree
Uses recursive-descent parsing algorithm

Grammar
=======
array_expr    : '[' array_list ']'

array_list    : element_list  ';' element_list
              | element_list

element_list  : element ',' element_list
              | element element_list
              | element

element       : NUMERIC_LITERAL
              | '-' NUMERIC_LITERAL

"""

from __future__ import unicode_literals
from lexer import Token
from errors import MatlabetteSyntaxError


class Parser(object):
    """
    Takes a list tokens and converts them to a parse tree
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    @property
    def token(self):
        return self.tokens[self.position]

    def match(self, token):
        return token == self.token[0]

    def consume(self):
        self.position += 1

    def expect(self, token):
        if self.match(token):
            self.consume()
            return True
        raise MatlabetteSyntaxError(self.token[1], token[0])

    def parse(self):
        if not self.match(Token.END_OF_LINE):
            node = ParseTreeNode(
                operator=u'=',
                left_child=ParseTreeNode(value='ans'),
                right_child=self.array_expression()
            )
            self.expect(Token.END_OF_LINE)
            return node
        return ParseTreeNode()

    def array_expression(self):
        """
        Implements the rule:
            array_expression : '[' array_list ']'
        """
        if self.match(Token.LEFT_SQUARE_BRACKET):
            self.consume()
            node = self.array_list()
            self.expect(Token.RIGHT_SQUARE_BRACKET)
        else:
            raise MatlabetteSyntaxError(
                self.token[1],
                Token.LEFT_SQUARE_BRACKET
            )
        return node

    def array_list(self):
        """
        Implements the rule:
            array_list : element_list  ';' element_list
                       | element_list
        """
        node = ParseTreeNode(value=[])
        while True:
            if self.match(Token.SEMI_COLON):
                self.consume()
            elements = self.element_list()
            if elements:
                if len(node.value) and len(node.value[-1]) != len(elements):
                    raise MatlabetteSyntaxError(self.token[1], "End of list not")
                node.value.append(elements)
            else:
                break
        return node

    def element_list(self):
        """
        Implements the rule:
            element_list  : element ',' element_list
                          | element element_list
                          | element

        """
        elements = []
        while True:
            if self.match(Token.COMMA):
                self.consume()
            element = self.array_element()
            if element is not None:
                elements.append(element)
            else:
                break
        return elements

    def array_element(self):
        """
        Implements the rule:
            element : NUMERIC_LITERAL
                    | '-' NUMERIC_LITERAL
        """
        value = None
        if self.match(Token.INTEGER_LITERAL):
            value = int(self.token[1])
            self.consume()
        elif self.match(Token.SUBTRACT_OPERATOR):
            self.consume()
            value = -self.array_element().value
        return value


class ParseTreeNode(object):
    """
    One node of the parse tree
    This defines the parse tree recursively
    """
    def __init__(self, **kwargs):
        self.operator = kwargs.get("operator")
        self.left_child = kwargs.get("left_child")
        self.right_child = kwargs.get("right_child")
        self.value = kwargs.get("value")
