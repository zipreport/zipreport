from argparse import ArgumentParser
from .base import CliCommand
from zipreport import get_version


class VersionCommand(CliCommand):
    usage = "[-m]"
    description = "Show version information"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "-m",
            "--minimal",
            help="only show version number",
            required=False,
            default=False,
            action="store_true",
        )

    def run(self, args) -> bool:
        if args.minimal:
            vstr = "{}"
        else:
            vstr = "\nVersion: {}\n"
        self.tty.message(vstr.format(get_version()))
        return True
