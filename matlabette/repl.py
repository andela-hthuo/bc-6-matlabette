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
        self.context = Context()

    def loop(self, message="matlabette> "):
        try:
            print("Matlabette, a tiny MATLAB clone")
            while True:
                line = self.prompt(message)
                self.eval(line)

        except KeyboardInterrupt:
            print("Exiting...")

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
            print(os.linesep, e.message, os.linesep)
