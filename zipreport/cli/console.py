import sys

from zipreport.cli.command import (
    DebugCommand,
    VersionCommand,
    ListCommand,
    HelpCommand,
    BuildCommand,
    InfoCommand,
)
from zipreport.cli.utils.argparse import ArgParser
from zipreport.cli.utils.console import ConsoleWriter


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    available_commands = {
        "help": HelpCommand,
        "version": VersionCommand,
        "list": ListCommand,
        "info": InfoCommand,
        "build": BuildCommand,
        "debug": DebugCommand,
    }

    # default command when no args detected
    command = "help"

    # extract command if specified
    if len(args) > 0:
        command = str(args.pop(0))

    writer = ConsoleWriter()
    parser = ArgParser()

    # list available commands
    if command == "help":
        writer.message("\navailable commands:\n")
        for cmd, cls in available_commands.items():
            writer.message("{:15} {:40} {}".format(cmd, cls.usage, cls.description))
        writer.message("\n")
        exit(0)

    # not list, lookup commands
    if command in available_commands.keys():
        handler = available_commands[command](writer=writer)

        if not handler.skipargs:  # skipargs controls usage of argparser
            handler.arguments(parser)
            args = parser.parse_args(args)
            if parser.failed:
                # invalid/insufficient args
                writer.error(parser.error_message)
                parser.print_help(writer.tty_error())
                exit(-2)
        else:
            # skipargs is true, all argparsing is ignored
            args = None

        exit(0 if handler.run(args) is True else -3)

    else:
        writer.error("error executing '{}': command not found".format(command))
        exit(-1)
