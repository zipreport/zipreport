from argparse import ArgumentParser

from zipreport.cli.utils.console import ConsoleWriter


class CliCommand:
    usage = ""  # parameter usage
    description = "command description"
    skipargs = False

    def __init__(self, writer=None):
        if not writer:
            writer = ConsoleWriter()
        self.tty = writer

    def arguments(self, parser: ArgumentParser):
        pass

    def run(self, args) -> bool:
        return True
