"""
Holds the state of the system
"""
from __future__ import unicode_literals, print_function
from operator import (
    add,
    sub,
    mul,
    div,
)
from errors import MatlabetteRuntimeError


class Context(object):

    def __init__(self):
        self.variables = {}
        self.operations = {
            u'+': add,
            u'-': sub,
            u'*': mul,
            u'/': div,
            u'=': self.assign
        }

    def evaluate(self, parse_tree):
        if parse_tree.value is not None:
            return parse_tree.value
        else:
            op = parse_tree.operator
            if op:
                action = self.operations[op]
                return action(
                    self.evaluate(parse_tree.left_child),
                    self.evaluate(parse_tree.right_child)
                )
            elif parse_tree.left_child:
                return self.evaluate(parse_tree.left_child)
            elif parse_tree.right_child:
                return self.evaluate(parse_tree.right_child)

    def assign(self, variable, value):
        self.variables[variable] = value
        self.output(variable)
        return self.variables[variable]

    def output(self, variable):
        if variable not in self.variables:
            raise MatlabetteRuntimeError("{} is not defined".format(variable))
        print("{} =".format(variable))
        value = self.variables[variable]
        if not len(value):
            print("\t", "[]")
        for row in value:
            print("\t", end='')
            for cell in row:
                print(cell, "\t", end='')
            print('')
        print('')
