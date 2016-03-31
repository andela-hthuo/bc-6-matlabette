"""
Holds the state of the system
"""
from __future__ import unicode_literals, print_function
from errors import MatlabetteRuntimeError
import os


class Context(object):

    def __init__(self, commands=None):
        self.variables = {}
        self.binary_operations = {
            u'=': self.assign
        }
        self.unary_operations = {
            u'show': self.show
        }
        self.commands = commands or {}

    def evaluate(self, parse_tree):
        """
        Walks the parse tree and determine the output expected from
        it
        """
        op = parse_tree.operator
        if op:
            if parse_tree.value is not None:
                action = self.unary_operations[op]
                value = parse_tree.value if parse_tree.locked \
                    else self.evaluate_value(parse_tree.value)
                return action(value)
            else:
                action = self.binary_operations[op]
                return action(
                    self.evaluate(parse_tree.left_child),
                    self.evaluate(parse_tree.right_child)
                )
        elif parse_tree.value is not None:
            if parse_tree.locked:
                return parse_tree.value
            return self.evaluate_value(parse_tree.value)
        elif parse_tree.left_child:
            return self.evaluate(parse_tree.left_child)
        elif parse_tree.right_child:
            return self.evaluate(parse_tree.right_child)

    def evaluate_value(self, node_value):
        """
        Return the value represented by a node value
        """
        # node_value is a variable name
        if isinstance(node_value, unicode):
            return self.dereference(node_value)

        # node_value is an array
        if isinstance(node_value, list):
            if not node_value:
                return node_value
            values = []
            column_count = len(node_value[0])
            for row in node_value:
                values_row = []
                for cell in row:
                    value = self.evaluate(cell)
                    if isinstance(value, list):
                        raise MatlabetteRuntimeError(
                            "Nested arrays not allowed"
                        )
                    values_row.append(value)
                if len(values_row) != column_count:
                    raise MatlabetteRuntimeError(
                        "Unequal column sizes"
                    )
                values.append(values_row)
            return values
        return node_value

    def dereference(self, variable):
        """
        Return value stored in variable
        """
        if variable not in self.variables:
            raise MatlabetteRuntimeError(
                "{} is not defined".format(variable)
            )
        return self.variables[variable]

    def assign(self, variable, value):
        """
        Assigns value to variable
        """
        if variable in self.commands:
            raise MatlabetteRuntimeError(
                "{} is reserved".format(variable)
            )
        self.variables[variable] = value
        return self.show(variable)

    def show(self, variable):
        """
        Generate string for displaying variable
        """
        if variable in self.commands:
            return self.commands[variable]()

        value = self.dereference(variable)
        output = "{}{} =".format(os.linesep, variable)
        spacer = "    "
        if isinstance(value, list):
            if value:
                output += os.linesep
                for row in value:
                    for cell in row:
                        output += "{}{}".format(spacer, cell)
                    output += os.linesep
            else:
                output += " []"
        else:
            output += " {}".format(value)
        return output + os.linesep
