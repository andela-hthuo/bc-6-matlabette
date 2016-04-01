"""
Takes a list tokens and converts them to a parse tree
Uses recursive-descent parsing algorithm

Grammar
=======
statement     : identifier '=' expr
              | identifier
expr          : array_expr
              | atom
array_expr    : '[' array_list ']'

array_list    : expr_list  ';' expr_list
              | expr_list

expr_list     : expr ',' expr_list
              | expr expr_list
              | expr

atom          : NUMERIC_LITERAL
              | '-' NUMERIC_LITERAL

identifier    : IDENTIFIER

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

    @property
    def token_type(self):
        return self.token[0]

    @property
    def token_value(self):
        return self.token[1]

    def match(self, token):
        return token == self.token_type

    def consume(self):
        self.position += 1

    def expect(self, token):
        if self.match(token):
            self.consume()
            return True
        raise MatlabetteSyntaxError(self.token_value, token)

    def parse(self):
        if self.match(Token.END_OF_LINE):
            return ParseTreeNode()
        parse_tree = self.statement()
        if parse_tree is None:
            parse_tree = ParseTreeNode(
                operator=u'=',
                left_child=ParseTreeNode(value='ans', locked=True),
                right_child=self.expression(True)
            )
        self.expect(Token.END_OF_LINE)
        return parse_tree

    def statement(self):
        """
        Implements the rule:
            statement     : identifier '=' expr
                          | identifier
        """
        identifier = self.identifier()
        if identifier is not None:
            if self.match(Token.END_OF_LINE):
                node = ParseTreeNode(
                    operator=u'show',
                    value=identifier,
                    locked=True
                )
                return node
            elif self.match(Token.ASSIGN_OPERATOR):
                self.consume()
                node = ParseTreeNode(
                    left_child=ParseTreeNode(value=identifier, locked=True),
                    operator=u'=',
                    right_child=self.expression(True)
                )
                return node
            elif self.match(Token.TRANSPOSE_OPERATOR):
                self.consume()
                node = ParseTreeNode(
                    left_child=ParseTreeNode(value=u'ans', locked=True),
                    operator=u'=',
                    right_child=ParseTreeNode(value=identifier, operator=u'\'')
                )
                return node
            else:
                op, sub_expr = self.sub_expression()
                if sub_expr is not None:
                    return ParseTreeNode(
                        left_child=ParseTreeNode(value=u'ans', locked=True),
                        operator=u'=',
                        right_child=ParseTreeNode(
                            operator=op,
                            left_child=ParseTreeNode(value=identifier),
                            right_child=sub_expr)
                    )
                op, sub_expr = self.sub_term()
                if sub_expr is not None:
                    return ParseTreeNode(
                        left_child=ParseTreeNode(value=u'ans', locked=True),
                        operator=u'=',
                        right_child=ParseTreeNode(
                            operator=op,
                            left_child=ParseTreeNode(value=identifier),
                            right_child=sub_expr)
                    )
                raise MatlabetteSyntaxError(
                    self.token_value,
                    Token.ASSIGN_OPERATOR
                )
        return None

    def expression(self, fail):
        """
        Implements: expression : array_expr | atom
        :param fail: if set to True, raise an exception instead of returning None
        """
        term = self.term()
        if term is not None:
            op, sub_expr = self.sub_expression()
            if sub_expr is not None:
                return ParseTreeNode(
                    operator=op,
                    left_child=term,
                    right_child=sub_expr
                )
            op, sub_expr = self.sub_term()
            if sub_expr is not None:
                return ParseTreeNode(
                    operator=op,
                    left_child=term,
                    right_child=sub_expr
                )
            return term
        if fail:
            raise MatlabetteSyntaxError(
                self.token_value,
                "[ or a number"
            )

    def sub_expression(self):
        node = ParseTreeNode()
        if self.match(Token.SUBTRACT_OPERATOR) \
                or self.match(Token.ADD_OPERATOR) \
                or self.match(Token.ELEM_SUBTRACT_OPERATOR) \
                or self.match(Token.ELEM_ADD_OPERATOR):
            operator = self.token_value
            self.consume()
            node.left_child = self.term()
            if not node.left_child:
                raise MatlabetteSyntaxError(
                    self.token_type,
                    "number"
                )
            node.operator, node.right_child = self.sub_expression()
            return operator, node
        return None, None

    def term(self):
        terminal = self.terminal()
        if terminal:
            op, sub_term = self.sub_term()
            if sub_term is not None:
                return ParseTreeNode(
                    operator=op,
                    left_child=terminal,
                    right_child=sub_term
                )
            return terminal
        return None

    def sub_term(self):
        node = ParseTreeNode()
        if self.match(Token.DIVIDE_OPERATOR) \
                or self.match(Token.MULTIPLY_OPERATOR) \
                or self.match(Token.ELEM_DIVIDE_OPERATOR) \
                or self.match(Token.ELEM_MULTIPLY_OPERATOR):
            operator = self.token_value
            self.consume()
            node.left_child = self.terminal()
            if not node.left_child:
                raise MatlabetteSyntaxError(
                    self.token_type,
                    "number"
                )
            node.operator, node.right_child = self.sub_term()
            return operator, node
        return None, None

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
            return None
        return node

    def array_list(self):
        """
        Implements the rule:
            array_list : expr_list  ';' expr_list
                       | expr_list
        """
        node = ParseTreeNode(value=[])
        while True:
            if self.match(Token.SEMI_COLON):
                self.consume()
            atoms = self.expression_list()
            if atoms:
                node.value.append(atoms)
            else:
                break
        return node

    def expression_list(self):
        """
        Implements the rule:
            expr_list     : expr ',' expr_list
                          | expr expr_list
                          | expr
        """
        expressions = []
        while True:
            if self.match(Token.COMMA):
                self.consume()
            expression = self.expression(False)
            if expression is not None:
                expressions.append(expression)
            else:
                break
        return expressions

    def terminal(self):
        node = None
        terminal = self.atom() or self.identifier()
        if terminal:
            node = ParseTreeNode(value=terminal)
        else:
            node = self.array_expression()
        if node and self.match(Token.TRANSPOSE_OPERATOR):
            node.operator = self.token_value
            self.consume()
        return node

    def identifier(self):
        """
        Implements the rule:
            identifier : IDENTIFIER
        """
        identifier = None
        if self.match(Token.VARIABLE_NAME) \
                or self.match(Token.BUILTIN_NAME):
            identifier = self.token_value
            self.consume()
        return identifier

    def atom(self):
        """
        Implements the rule:
            atom : NUMERIC_LITERAL
                 | '-' NUMERIC_LITERAL
        """
        value = None
        if self.match(Token.INTEGER_LITERAL) \
                or self.match(Token.FLOAT_LITERAL):
            value = float(self.token_value)
            self.consume()
        elif self.match(Token.SUBTRACT_OPERATOR):
            self.consume()
            value = -self.atom()
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
        self.locked = kwargs.get("locked", False)
