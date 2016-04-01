"""
Operators
"""
from errors import InvalidArgumentsForOperator


class Operators(object):

    @staticmethod
    def add(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def subtract(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def multiply(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs * rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def divide(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def elem_add(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def elem_subtract(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def elem_multiply(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs * rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def elem_divide(lhs, rhs):
        if isinstance(lhs, float) and isinstance(rhs, float):
            return lhs + rhs
        raise InvalidArgumentsForOperator

    @staticmethod
    def transpose(array):
        return array
