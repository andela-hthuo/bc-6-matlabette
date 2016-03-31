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
                return action(parse_tree.value)
            else:
                action = self.binary_operations[op]
                return action(
                    self.evaluate(parse_tree.left_child),
                    self.evaluate(parse_tree.right_child)
                )
        elif parse_tree.value is not None:
            return parse_tree.value
        elif parse_tree.left_child:
            return self.evaluate(parse_tree.left_child)
        elif parse_tree.right_child:
            return self.evaluate(parse_tree.right_child)

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

        if variable not in self.variables:
            raise MatlabetteRuntimeError(
                "{} is not defined".format(variable)
            )

        value = self.variables[variable]
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
