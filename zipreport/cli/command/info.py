from argparse import ArgumentParser
from pathlib import Path

from .base import CliCommand
from zipreport.report import ReportFileLoader, const


class InfoCommand(CliCommand):
    usage = "<file> [<file>...]"
    description = "Show report details"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "file", type=str, help="list of file(s) to show info", nargs="*"
        )

    def run(self, args) -> bool:
        if len(args.file) == 0:
            self.tty.error("Error: no file specified")
            return False

        for fn in args.file:
            path = Path(fn)

            if not path.exists():
                self.tty.error("Error: Invalid path")
                return False

            if not path.is_file():
                self.tty.error("Error: Path {} is not a valid file".format(path))
                return False

            try:
                path = str(path)
                zpt = ReportFileLoader.load_file(path)
                self.tty.message(
                    "{:30} {}".format(path, zpt.get_param(const.MANIFEST_TITLE, ""))
                )
            except Exception as e:
                self.tty.error("Error: {} is not a valid zipreport file".format(path))
        return True
