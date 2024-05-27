from argparse import ArgumentParser
from .base import CliCommand


class HelpCommand(CliCommand):
    description = "Show usage information"

    def arguments(self, parser: ArgumentParser):
        pass

    def run(self, args) -> bool:
        return True
