import os
from argparse import ArgumentParser
from pathlib import Path

from .base import CliCommand
from zipreport.report import ReportFileLoader, const


class ListCommand(CliCommand):
    usage = "<path>"
    description = "List reports on the given path"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "path",
            type=str,
            help="path to list reports",
            nargs="?",
            default=os.getcwd(),
        )
        parser.add_argument(
            "-s",
            "--symlinks",
            help="follow symlinks",
            required=False,
            default=False,
            action="store_true",
        )

    def run(self, args) -> bool:
        path = Path(args.path)
        if not path.exists():
            self.tty.error("Error: Invalid path '{}'".format(path))
            return False

        if not path.is_dir():
            self.tty.error("Error: Path '{}' is not a valid directory".format(path))
            return False

        for dirpath, dirnames, filenames in os.walk(path, followlinks=args.symlinks):
            for f in filenames:
                if f.endswith(".zpt"):
                    try:
                        fpath = os.path.join(dirpath, f)
                        zpt = ReportFileLoader.load_file(fpath)
                        self.tty.message(
                            "{:30} {}".format(
                                f, zpt.get_param(const.MANIFEST_TITLE, "")
                            )
                        )

                    except Exception:
                        # ignore file
                        pass
        return True
