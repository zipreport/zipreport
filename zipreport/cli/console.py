import os
from pathlib import Path

import sys

from zipreport.cli.debug.server import DebugServer
from zipreport.report import ReportFileBuilder, ReportFileLoader, const
from zipreport.version import get_version


class Commands:
    EXT = '.zpt'
    HELP_LINE = "  %-30s %s\n"
    LIST_LINE = "%-20s %s"
    COMMANDS = {
        'help': ['', 'Show usage information'],
        'version': ['[-m]', 'Show version (or version number only, if -m)'],
        'list': ['<path>', 'List reports on the given path'],
        'info': ['<file> [<file>...]', 'Show report details'],
        'build': ['<directory> [output_file]', 'Build zpt file bundle'],
        'debug': ['<directory|file> [[host]:<port>]', 'Run debug server using the directory or specified file'],
    }

    def run(self, args: list):
        if len(args) == 0:
            self.help([])
            return 0

        cmd = args[0]
        method = getattr(self, cmd, None)
        if not callable(method):
            self.error("Error: invalid command {}".format(cmd))
            return 1

        if method(args[1:]) is False:
            return 1

        return 0

    def version(self, args=None):
        minimal = len(args) == 1 and args[0] == '-m'
        if minimal:
            vstr = "{}"
        else:
            vstr = "\nVersion: {}\n"
        print(vstr.format(get_version()))

    def help(self, args=None):
        if len(args) == 1:
            cmd = args[0]
            if cmd in self.COMMANDS.keys():
                print("\n{cmd} usage:".format(cmd=cmd))
                usage = cmd + " " + self.COMMANDS[cmd][0]
                print(self.HELP_LINE % (usage, self.COMMANDS[cmd][1]))
            else:
                # this shouldn't actually happen, as commands are pre-checked
                self.error("Error: invalid command {}".format(cmd))
            return

        help = ""
        for k, v in self.COMMANDS.items():
            usage = " ".join([k, v[0]])
            help += self.HELP_LINE % (usage, v[1])
        print("\nUsage:\n{}\n\n".format(help))

    def build(self, args) -> bool:
        if len(args) == 0 or len(args) > 2:
            self.error("Error: Invalid command syntax")
            return False

        src = Path(args[0]).resolve()
        if not src.exists() or not src.is_dir():
            self.error("Error: {path} is not a valid folder".format(path=str(src)))
            return False

        if len(args) == 2:
            dest = Path(args[1]).resolve()
        else:
            dest = Path(src.name)

        if dest.suffix == '':
            dest = dest.with_suffix(self.EXT)

        result = ReportFileBuilder.build_file(src, dest)
        if not result.success():
            self.error(" ".join(result.get_errors()))
        return result.success()

    def debug(self, args) -> bool:
        if len(args) == 0 or len(args) > 3:
            self.error("Error: Invalid command syntax")
            return False

        source = Path(args[0])
        if not source.exists():
            self.error("Error: Specified path not found")
            return False

        host = DebugServer.DEFAULT_ADDR
        port = DebugServer.DEFAULT_PORT

        if len(args) > 2:
            host = args[1]
            port = args[2]
        elif len(args) == 2:
            port = args[1]

        DebugServer(host, port).run(source)

    def list(self, args) -> bool:
        if len(args) > 1:
            self.error("Error: Invalid command syntax")
            return False
        if len(args) == 0:
            path = Path(os.getcwd())
        else:
            path = Path(args[0])

        if not path.exists():
            self.error("Error: Invalid path")
            return False
        if not path.is_dir():
            self.error("Error: Path is not a valid directory")
            return False

        for (dirpath, dirnames, filenames) in os.walk(path):
            for f in filenames:
                if f.endswith('.zpt'):
                    try:
                        zpt = ReportFileLoader.load_file(f)
                        print(self.LIST_LINE % (f, zpt.get_param(const.MANIFEST_TITLE, "")))
                    except Exception:
                        # ignore file
                        pass
        return True

    def info(self, args) -> bool:
        if len(args) == 0:
            self.error("Error: Invalid command syntax")
            return False

        for fn in args:
            path = Path(fn)

            if not path.exists():
                self.error("Error: Invalid path")
                return False

            if not path.is_file():
                self.error("Error: Path {} is not a valid file".format(path))
                return False

            try:
                zpt = ReportFileLoader.load_file(path)
                print(self.LIST_LINE % (path, zpt.get_param(const.MANIFEST_TITLE, "")))
            except Exception:
                self.error("Error: {} is not a valid zipreport file".format(path))
        return True

    def error(self, message):
        sys.stderr.write("\n{msg}\n\n".format(msg=message))


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    cli = Commands()
    exit(cli.run(args))
