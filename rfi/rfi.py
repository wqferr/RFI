#!/usr/bin/env python3
"""RFI repl and main logic."""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.utils import test_callable_args


class Repl:  # pylint: disable=too-few-public-methods,no-self-use
    """REPL for RFI."""

    commands = {
        "help": "Display help for all commands.",
        "add": "Add turn to initiative order. Usage: add {name} {initiative}",
    }  # TODO "remove", "chname", "chroll", "mv", "start", "next", "prev", "clear"

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

            cmd_function_name = "_" + cmd
            try:
                cmd_function = getattr(self, cmd_function_name)
                assert test_callable_args(cmd_function, cmd_args)
                cmd_function(*cmd_args)
            except AttributeError:
                print(f"Unknown command: {cmd}.")
                continue
            except AssertionError:
                print(f"Invalid arguments for {cmd}. Type help for more information.")

    def _get_command_function(self, cmd: str):
        return getattr(self, f"_{cmd}")

    def _help(self):
        for cmd, cmd_help in self.commands.items():
            print(cmd, cmd_help, sep="\t")

    def _add(self, name, initiative):
        print(initiative, name)


def main():
    """Create a rfi.Repl instance and run it."""
    Repl().run()


if __name__ == "__main__":
    main()
