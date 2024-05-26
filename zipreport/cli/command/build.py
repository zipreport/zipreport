from argparse import ArgumentParser
from pathlib import Path

from .base import CliCommand
from zipreport.report import ReportFileBuilder


class BuildCommand(CliCommand):
    ext = ".zpt"
    usage = "<directory> [file] [-s]"
    description = "Build zpt file bundle"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("directory", type=str, help="directory to build")
        parser.add_argument("file", type=str, help="output file", nargs="?", default="")
        parser.add_argument(
            "-s",
            "--symlinks",
            help="follow template symlinks when building",
            required=False,
            default=False,
            action="store_true",
        )

    def run(self, args) -> bool:
        src = Path(args.directory).resolve()
        if not src.exists() or not src.is_dir():
            self.tty.error("Error: {path} is not a valid folder".format(path=str(src)))
            return False

        dest = Path(src.name)
        if args.file != "":
            dest = Path(args.file).resolve()

        if dest.suffix == "":
            dest = dest.with_suffix(self.ext)

        result = ReportFileBuilder.build_file(
            str(src), str(dest), follow_links=args.symlinks
        )
        if not result.success():
            self.tty.error(" ".join(result.get_errors()))
        return result.success()
