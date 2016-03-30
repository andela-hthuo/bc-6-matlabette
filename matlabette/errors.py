"""
Contains custom exceptions for matlabette errors
"""


class MatlabetteError(Exception):
    """
    Exception for matlabette errors
    """
    pass


class MatlabetteSyntaxError(MatlabetteError):
    """
    Exception for matlabette syntax errors
    """
    def __init__(self, current_token, expected_token):
        self.current_token = current_token.replace(u'\n', "end of line")
        self.expected_token = expected_token
        self.message = "Syntax error near '{}'. {} expected".format(
            self.current_token,
            self.expected_token
        )


class MatlabetteRuntimeError(MatlabetteError):
    """
    Exception for matlabette runtime errors
    """
    pass
