"""
Manages the read-eval-print loop
"""
from __future__ import unicode_literals, print_function
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments.lexers.matlab import MatlabLexer
from colorama import Fore, init

from lexer import Lexer
from parser import Parser
from errors import MatlabetteError
from context import Context
import os

init()


class Repl(object):
    default_workspace = "workspace.mat"

    def __init__(self):
        self.history = FileHistory('.history')
        self.context = Context({
            u'help': self.help,
            u'exit': self.exit,
            u'save': self.save,
            u'load': self.load_default,
        })

    def loop(self, message="matlabette> "):
        try:
            print (Fore.BLUE)
            print(""" Matlabette, a tiny MATLAB clone.
 Type exit or press Ctrl + C / Ctrl + D to exit.
 Type help for help.""")
            print ()
            while True:
                line = self.prompt(message)
                self.eval(line)

        except (KeyboardInterrupt, EOFError):
            self.exit_prompt()

    def prompt(self, message):
        return prompt(
            message,
            history=self.history,
            auto_suggest=AutoSuggestFromHistory(),
            lexer=MatlabLexer,
            display_completions_in_columns=True,
            mouse_support=True
        )

    def exit_prompt(self):
        try:
            while True:
                option = self.prompt("Save the workspace? (y/n) ").lower()
                if option == 'y':
                    self.save()
                    break
                elif option == 'n':
                    raise KeyboardInterrupt
        except (KeyboardInterrupt, EOFError):
            print (Fore.YELLOW)
            print (" Workspace not saved")
            print ()

    def eval(self, line):
        if line.startswith("save "):
            filename = line.replace("save ", "")
            self.save(filename)
            return

        if line.startswith("load "):
            filename = line.replace("load ", "")
            self.load(filename)
            return

        tokens = Lexer.lex(line)
        try:
            parse_tree = Parser(tokens).parse()
            if parse_tree:
                output = self.context.evaluate(parse_tree)
                if output:
                    print(Fore.GREEN + output)

        except MatlabetteError as e:
            print(Fore.RED)
            print(" Error: " + e.message)
            print()

    def load(self, filename):
        print ()
        try:
            with open(filename, 'r') as f:
                print(Fore.BLUE + " Loading workspace from '{}'"
                      .format(os.path.abspath(filename)))
                input_line = f.readline()
                while input_line:
                    self.eval(input_line)
                    input_line = f.readline()
                print(Fore.BLUE + " Done")
        except IOError:
            print(Fore.RED + " Error: failed to open '{}'"
                  .format(os.path.abspath(filename)))
        print ()

    def load_default(self):
        if os.path.isfile(self.default_workspace):
            self.load(self.default_workspace)
        else:
            print (Fore.YELLOW)
            print(" Default workspace doesn't exist. To create it, type save")
            print ()

    def save(self, filename=default_workspace):
        print()
        try:
            with open(filename, 'w') as f:
                f.write(self.context.serialize())
                print(Fore.BLUE + " Workspace saved to '{}'"
                      .format(os.path.abspath(filename)))
        except IOError:
            print(Fore.RED + " Error: failed to open '{}'"
                  .format(os.path.abspath(filename)))
        print()

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
