#!/usr/bin/env python3
"""RFI repl and main logic."""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.utils import test_callable_args
from texttable import Texttable


class Repl:  # pylint: disable=too-few-public-methods,no-self-use
    """REPL for RFI."""

    commands_usage = {
        "help": "help [command]",
        "add": "add {name} {initiative}",
        "remove": "remove {name}",
        "chname": "chname {current_name} {new_name}",
        "chinit": "chinit {name} {new_initiative}",
        "start": "start",
        "done": "done",
        "back": "back",
        "mv": "mv {name} (up|down)",
        "clear": "clear",
    }
    commands = list(commands_usage.keys())

    def __init__(self):
        """See help(Repl) for more information."""
        completer = WordCompleter(self.commands, sentence=True)
        self.session = PromptSession("> ", completer=completer)
        # TODO self.turns = InitiativeQueue

    def run(self):
        """Run the REPL until EOF is reached."""
        while True:
            try:
                user_input = self.session.prompt()
                cmd, *cmd_args = user_input.split()
            except (KeyboardInterrupt, ValueError):
                # Invalid input string
                continue
            except EOFError:
                break

            try:
                cmd_function = self._get_command_function(cmd)
            except AttributeError:
                print(f"Unknown command: {cmd}.")
                continue

            if not test_callable_args(cmd_function, cmd_args):
                print()
                print(f"Invalid usage of {cmd}.")
                print(f"Expected usage: {self.commands_usage[cmd]}")
                print(f"Type help {cmd} for more information.")
                print()
                continue

            try:
                cmd_function(*cmd_args)
            except ValueError as err:
                print(f"Error: {err}")
                print()

    def _get_command_function(self, cmd: str):
        return getattr(self, f"cmd_{cmd}")

    def _help_all(self):
        table = Texttable()
        table.set_cols_align("lcl")
        table.header(["Command", "Description", "Usage"])
        table.set_deco(table.HEADER | table.VLINES)
        table.set_max_width(90)
        for cmd, cmd_usage in self.commands_usage.items():
            cmd_help = self._get_cmd_help(cmd)
            if cmd_help is not None:
                table.add_row([cmd, cmd_help, cmd_usage])
        print(table.draw())

    def _help_single(self, cmd):
        cmd_help = self._get_cmd_help(cmd)
        if cmd_help is None:
            raise ValueError(f"No help available for command {cmd}")
        print(cmd_help)
        print(f"Usage: {self.commands_usage[cmd]}")

    def _get_cmd_help(self, cmd):
        try:
            return self._get_command_function(cmd).__doc__
        except AttributeError:
            return None

    def cmd_help(self, cmd=None):
        """Display help for one or all commands."""
        print()
        if cmd is None:
            self._help_all()
        else:
            self._help_single(cmd)
        print()

    def cmd_add(self, name, initiative):
        """Add turn to initiative order."""

    def cmd_remove(self, name):
        """Remove a turn from initiative order."""

    def cmd_chname(self, current_name, new_name):
        """Rename an existing turn."""

    def cmd_chinit(self, name, new_initiative):
        """Reassign initiative to an existing turn."""

    def cmd_start(self):
        """Initialize the cursor, pointing it to the first turn in initiative order."""

    def cmd_done(self):
        """Advance cursor to the next turn."""

    def cmd_back(self):
        """Move cursor back one position."""

    def cmd_mv(self, name, direction):
        """Reorder turns with tied initiative, moving one of them up or down."""

    def cmd_clear(self):
        """Reset initiative queue."""


def main():
    """Create a rfi.Repl instance and run it."""
    Repl().run()


if __name__ == "__main__":
    main()
