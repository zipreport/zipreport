import importlib, importlib.util
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Callable, Union, Optional

from .base import CliCommand
from zipreport.cli.debug.server import DebugServer
from zipreport.template import EnvironmentWrapper


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
        parser.add_argument(
            "-w",
            "--wrapper",
            type=str,
            help="wrapper class (file.class_name or module.class_name)",
            default="",
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

    def load_module(self, path) -> Optional[Union[bool, Callable]]:
        module_path, cls_name = path.rsplit(".", 1)
        if importlib.util.find_spec(module_path) is not None:
            module = importlib.import_module(module_path)
            # return class or None
            return getattr(module, cls_name, None)
        else:
            # not found, return False
            return False

    def load_file(self, path) -> Optional[Union[bool, Callable]]:
        fname, cls_name = path.rsplit(".", 1)
        fpath = Path(fname + ".py")
        if not fpath.exists() or not fpath.is_file():
            return False
        try:
            with TempSysPath(fpath.parent):
                spec = importlib.util.spec_from_file_location(fname, fpath)
                module = importlib.util.module_from_spec(spec)
                # sys.modules["_zipreport_wrapper_"] = module
                spec.loader.exec_module(module)
                cls = getattr(module, cls_name, None)
                return cls
        except FileNotFoundError:
            # not found, return False
            return False

    def run(self, args) -> bool:
        source = Path(args.path)
        if not source.exists():
            self.tty.error("Error: Specified path not found")
            return False

        valid, host, port = self.parse_hostport(args.hostport)
        if not valid:
            self.tty.error("Error: Invalid host:port '{}'".format(args.hostport))
            return False

        wrapper = None
        if len(args.wrapper) > 0:
            # first, attempt to load module
            cls = self.load_module(args.wrapper)
            if cls is None:
                module_path, cls_name = args.wrapper.rsplit(".", 1)
                self.tty.error(
                    "Error: could not find class '{}' inside module '{}'".format(
                        cls_name, module_path
                    )
                )
                return False

            if cls is False:
                # module loading did not work, lets try via file
                cls = self.load_file(args.wrapper)
                module_path, cls_name = args.wrapper.rsplit(".", 1)
                if cls is None:
                    self.tty.error(
                        "Error: could not find class '{}' inside file '{}.py'".format(
                            cls_name, module_path
                        )
                    )
                    return False

                if cls is False:
                    self.tty.error(
                        "Error: could not find file '{}.py'".format(module_path)
                    )
                    return False

            wrapper = cls()
            if not isinstance(wrapper, EnvironmentWrapper):
                self.tty.error(
                    "Error: '{}' does not extend zipreport.template.EnvironmentWrapper".format(
                        str(wrapper.__class__)
                    )
                )
                return False

        DebugServer(host, port).run(source, follow_links=args.symlinks, wrapper=wrapper)
        return True

class TempSysPath:
    """Temporarily adjust sys.path to include a path."""
    def __init__(self, path: Path | str):
        self.path = str(path)

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.path.pop(0)