from argparse import ArgumentParser
from pathlib import Path

from .base import CliCommand
from zipreport.cli.debug.server import DebugServer


class DebugCommand(CliCommand):
    usage = "<directory|file> [host[:port]] [-s]"
    description = "Run debug server using the directory or specified file"

    def arguments(self, parser: ArgumentParser):
        hostport = "{}:{}".format(DebugServer.DEFAULT_ADDR, DebugServer.DEFAULT_PORT)
        parser.add_argument("path", type=str, help="directory or file")
        parser.add_argument(
            "hostport",
            type=str,
            help="<host>[:port] for the debug server (default {})".format(hostport),
            nargs="?",
            default=hostport,
        )
        parser.add_argument(
            "-s",
            "--symlinks",
            help="follow symlinks",
            required=False,
            default=False,
            action="store_true",
        )

    def parse_hostport(self, hostport: str):
        host = DebugServer.DEFAULT_ADDR
        port = DebugServer.DEFAULT_PORT
        if hostport.find(":") > -1:
            parts = hostport.split(":")
            if len(parts) != 2:
                return False, host, port
            if not parts[1].isdigit():
                return False, host, port
            host = parts[0].strip()
            port = parts[1]
        else:
            host = hostport

        return True, host, port

    def run(self, args) -> bool:
        source = Path(args.path)
        if not source.exists():
            self.tty.error("Error: Specified path not found")
            return False

        valid, host, port = self.parse_hostport(args.hostport)
        if not valid:
            self.tty.error("Error: Invalid host:port '{}'".format(args.hostport))
            return False

        DebugServer(host, port).run(source, follow_links=args.symlinks)
        return True
