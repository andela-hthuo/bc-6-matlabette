"""
Manages the read-eval-print loop
"""
from __future__ import unicode_literals, print_function
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from pygments.lexers.matlab import MatlabLexer
from colorama import Fore, init
from prompt_toolkit.contrib.completers import WordCompleter

from lexer import Lexer
from parser import Parser
from errors import MatlabetteError
from context import Context
import os
import re

init()
home = os.environ.get("HOME") or os.environ.get("USERPROFILE")
workspace, history = None, None
if home:
    matlabette_dir = os.path.join(home, '.matlabette')
    if not os.path.isdir(matlabette_dir):
        os.mkdir(matlabette_dir)
    if matlabette_dir:
        workspace = os.path.join(matlabette_dir, 'workspace')
        if not os.path.isfile(workspace):
            open(workspace, 'w').close()
        history = os.path.join(matlabette_dir, 'history')
workspace_file = workspace or 'workspace'
history_file = history or 'history'


class Repl(object):
    def __init__(self):
        self.history = FileHistory(history_file)
        self.context = Context({
            u'help': self.help,
            u'exit': self.exit,
            u'save': self.save,
            u'load': self.load_default,
        })

    @staticmethod
    def get_word_completer():
        if os.path.isfile(history_file):
            _file = open(history_file)
            history_list = _file.read().split('\n')
            history_list = [
                re.sub(r'#.*', '',  re.sub('^\+', '', i))
                for i in history_list
                ]
            return WordCompleter(list(set(history_list)), ignore_case=True)

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
            if self.context.variables:
                self.exit_prompt()

    def prompt(self, message):
        return prompt(
            message,
            history=self.history,
            lexer=MatlabLexer,
            completer=self.get_word_completer(),
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
        if os.path.isfile(workspace_file):
            self.load(workspace_file)
        else:
            print (Fore.YELLOW)
            print(" Default workspace doesn't exist. To create it, type save")
            print ()

    def save(self, filename=workspace_file):
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

Matlabette is a tiny MATLAB clone.
It implements the following functionality:

Array creation
==============

    a = [1, 2]
    b = [10 30; 40 50]

Array and matrix operations
===========================
Transpose
---------
    a = [1 2]
    a'

Dot product
-----------
    a = [3 2]
    b = [4; 3]
    a * b

Element-wise operations
-----------------------
    a = [7 8]
    b = [4 3]
    a .* b
    a + 1
    a - b

Inverse
-------
    inv([2 0; 0 2])

Save and load workspace
=======================
    save <filename>
    load <filename>
"""


