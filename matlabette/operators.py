"""
Operators
"""
from errors import InvalidArgumentsForOperator, MatlabetteRuntimeError
import numpy


class Operators(object):

    @staticmethod
    def add(lhs, rhs):
        if isinstance(lhs, float):
            if isinstance(rhs, float):
                return lhs + rhs
            if isinstance(rhs, list):
                return (numpy.array(rhs) + lhs).tolist()
        elif isinstance(lhs, list):
            if isinstance(rhs, float):
                return (numpy.array(lhs) + rhs).tolist()
            if isinstance(rhs, list):
                return (numpy.array(lhs) + numpy.array(rhs)).tolist()
        raise InvalidArgumentsForOperator

    @staticmethod
    def subtract(lhs, rhs):
        if isinstance(lhs, float):
            if isinstance(rhs, float):
                return lhs - rhs
            if isinstance(rhs, list):
                return (numpy.array(rhs) - lhs).tolist()
        elif isinstance(lhs, list):
            if isinstance(rhs, float):
                return (numpy.array(lhs) - rhs).tolist()
            if isinstance(rhs, list):
                return (numpy.array(lhs) - numpy.array(rhs)).tolist()
        raise InvalidArgumentsForOperator

    @staticmethod
    def multiply(lhs, rhs):
        if isinstance(lhs, float):
            if isinstance(rhs, float):
                return lhs * rhs
            if isinstance(rhs, list):
                return (numpy.array(rhs) * lhs).tolist()
        elif isinstance(lhs, list):
            if isinstance(rhs, float):
                return (numpy.array(lhs) * rhs).tolist()
            if isinstance(rhs, list):
                return (numpy.array(lhs).dot(numpy.array(rhs))).tolist()
        raise InvalidArgumentsForOperator

    @staticmethod
    def divide(lhs, rhs):
        if isinstance(lhs, float):
            if isinstance(rhs, float):
                return lhs / rhs
            if isinstance(rhs, list):
                return (numpy.array(rhs) / lhs).tolist()
        elif isinstance(lhs, list):
            if isinstance(rhs, float):
                return (numpy.array(lhs) / rhs).tolist()
            if isinstance(rhs, list):
                return (numpy.array(lhs) / numpy.array(rhs)).tolist()
        raise InvalidArgumentsForOperator

    @staticmethod
    def elem_add(lhs, rhs):
        return Operators.add(lhs, rhs)

    @staticmethod
    def elem_subtract(lhs, rhs):
        return Operators.subtract(lhs, rhs)

    @staticmethod
    def elem_multiply(lhs, rhs):
        if isinstance(lhs, list) and isinstance(rhs, list):
            return (numpy.array(lhs) * numpy.array(rhs)).tolist()
        return Operators.multiply(lhs, rhs)

    @staticmethod
    def elem_divide(lhs, rhs):
        return Operators.multiply(lhs, rhs)

    @staticmethod
    def transpose(array):
        return numpy.array(array).T.tolist()

    @staticmethod
    def invert(matrix_array):
        if len(matrix_array) != 1:
            raise MatlabetteRuntimeError('inv takes only one argument')
        if not isinstance(matrix_array[0], list):
            raise MatlabetteRuntimeError('Invalid argument for inv')
        return numpy.linalg.inv(matrix_array[0]).tolist()

    @staticmethod
    def transpose_function(matrix_array):
        if len(matrix_array) != 1:
            raise MatlabetteRuntimeError('transpose takes only one argument')
        if not isinstance(matrix_array[0], list):
            raise MatlabetteRuntimeError('Invalid argument for transpose')
        return Operators.transpose(matrix_array[0])
