"""
Manages the read-eval-print loop
"""
from __future__ import unicode_literals, print_function
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from lexer import Lexer
from parser import Parser
from errors import MatlabetteError
from context import Context
import os


class Repl(object):
    def __init__(self):
        self.history = FileHistory('.history')
        self.context = Context({
            u'help': self.help,
            u'exit': self.exit,
        })

    def loop(self, message="matlabette> "):
        try:
            print(""" Matlabette, a tiny MATLAB clone.
 Type exit or press Ctrl + C / Ctrl + D to exit.
 Type help for help.""")
            while True:
                line = self.prompt(message)
                self.eval(line)

        except (KeyboardInterrupt, EOFError):
            print("Exiting...", os.linesep)

    def prompt(self, message):
        return prompt(
            message,
            history=self.history,
            auto_suggest=AutoSuggestFromHistory(),
        )

    def eval(self, line):
        tokens = Lexer.lex(line)
        try:
            parse_tree = Parser(tokens).parse()
            if parse_tree:
                output = self.context.evaluate(parse_tree)
                print(output)

        except MatlabetteError as e:
            print(os.linesep, "Error:", e.message, os.linesep)

    @staticmethod
    def exit():
        raise KeyboardInterrupt

    @staticmethod
    def help():
        return """

Welcome to Matlabette!

Matlabette is a tiny clone.
It implements the following functionality:

    - array creation
    - array and matrix operations
    - concatenation
    - saving and loading workspaces

To learn more about the first three, go to:
    https://www.mathworks.com/help/matlab/learn_matlab/matrices-and-arrays.html

To save your workspace, use save <filename>.
To load workspace from file, use load <filename>
"""
