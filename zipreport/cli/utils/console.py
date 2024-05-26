import sys


class ConsoleWriter:
    def __init__(self):
        pass

    def message(self, message):
        self.tty_term().write("{msg}\n".format(msg=message))

    def error(self, message):
        self.tty_error().write("{msg}\n".format(msg=message))

    def tty_error(self):
        return sys.stderr

    def tty_term(self):
        return sys.stdout
