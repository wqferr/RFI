#!/usr/bin/env python3
"""RFI repl and main logic."""

from dice import roll
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.utils import test_callable_args
from texttable import Texttable

from rfi import InitiativeQueue
from rfi import __version__ as rfi_version


def _dice_roll_sum(dice_expr: str):
    result = roll(dice_expr)
    try:
        return sum(result)
    except TypeError:
        return result


class Repl:  # pylint: disable=too-few-public-methods,no-self-use
    """REPL for RFI."""

    commands_usage = {
        "help": "help [command]",
        "add": "add {name} {initiative_expression}",
        "remove": "remove {name}",
        "chname": "chname {current_name} {new_name}",
        "chinit": "chinit {name} {new_initiative_expression}",
        "start": "start",
        "next": "next",
        "prev": "prev",
        "move": "move {name} (up|down)",
        "clear": "clear",
        "show": "show",
    }
    commands = list(commands_usage.keys())

    def __init__(self):
        """See help(Repl) for more information."""
        completer = WordCompleter(self.commands, sentence=True)
        self.session = PromptSession("> ", completer=completer)
        self.queue = InitiativeQueue()
        self.cursor_pos = None

    def run(self):
        """Run the REPL until EOF is reached."""
        print(f"rfi version {rfi_version}")
        print("Type help and press enter for a list of commands.")
        print("Roll for initiative!")
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

    def cmd_help(self, cmd: str = None):
        """Display help for one or all commands."""
        print()
        if cmd is None:
            self._help_all()
        else:
            self._help_single(cmd)
        print()

    def cmd_add(self, name: str, initiative_expression: str):
        """Add turn to initiative order."""
        initiative = _dice_roll_sum(initiative_expression)
        self.queue.add(name, initiative)
        try:
            if self.queue.position_of(name) <= self.cursor_pos:
                self._move_cursor(+1)
        except TypeError:
            pass
        self._show_queue()

    def cmd_remove(self, name: str):
        """Remove a turn from initiative order."""
        try:
            if self.queue.position_of(name) < self.cursor_pos:
                self._move_cursor(-1)
        except TypeError:
            pass
        self.queue.remove(name)
        if self.cursor_pos is not None:
            self._move_cursor(0)
        self._show_queue()

    def cmd_chname(self, current_name: str, new_name: str):
        """Rename an existing turn."""
        self.queue.update_name(current_name, new_name)
        self._show_queue()

    def cmd_chinit(self, name: str, new_initiative_expression: str):
        """Reassign initiative to an existing turn."""
        new_initiative = _dice_roll_sum(new_initiative_expression)
        self.queue.update(name, new_initiative)
        self._show_queue()

    def cmd_start(self):
        """Initialize the cursor, pointing it to the first turn in initiative order."""
        self.cursor_pos = 0
        self._show_queue()

    def cmd_next(self):
        """Advance cursor to the next turn."""
        try:
            self._move_cursor(+1)
            self._show_queue()
        except TypeError:
            raise ValueError("Attempt to move cursor before call to start")

    def cmd_prev(self):
        """Move cursor prev one position."""
        try:
            self._move_cursor(-1)
            self._show_queue()
        except TypeError:
            raise ValueError("Attempt to move cursor before call to start")

    def cmd_move(self, name: str, direction: str):
        """Reorder turns with tied initiative, moving one of them up or down."""
        if direction == "up":
            self.queue.move_up(name)
            self._show_queue()
        elif direction == "down":
            self.queue.move_down(name)
            self._show_queue()
        else:
            raise ValueError("Direction must be up or down")

    def cmd_clear(self):
        """Reset initiative queue."""
        self.queue.clear()
        self._show_queue()

    def cmd_show(self):
        """Show current state of initiative queue."""
        if self.queue is None:
            raise ValueError("Start command not given yet")
        self._show_queue()

    def _make_table(self):
        table = Texttable()
        table.set_max_width(90)
        return table

    def _get_command_function(self, cmd: str):
        return getattr(self, f"cmd_{cmd}")

    def _help_all(self):
        table = self._make_table()
        table.set_deco(Texttable.HEADER | Texttable.VLINES)
        table.header(["Command", "Description", "Usage"])
        table.set_cols_align("lcl")
        for cmd, cmd_usage in self.commands_usage.items():
            cmd_help = self._get_cmd_help(cmd)
            if cmd_help is not None:
                table.add_row([cmd, cmd_help, cmd_usage])
        print(table.draw())

    def _help_single(self, cmd: str):
        cmd_help = self._get_cmd_help(cmd)
        if cmd_help is None:
            raise ValueError(f"No help available for command {cmd}")
        print(cmd_help)
        print(f"Usage: {self.commands_usage[cmd]}")

    def _get_cmd_help(self, cmd: str):
        try:
            return self._get_command_function(cmd).__doc__
        except AttributeError:
            return None

    def _move_cursor(self, delta: int):
        if self.queue:
            self.cursor_pos += delta + len(self.queue)
            self.cursor_pos %= len(self.queue)
        else:
            self.cursor_pos = None

    def _show_queue(self):
        if self.queue:
            table = self._make_table()
            table.set_deco(0)
            for position, (name, initiative) in enumerate(self.queue):
                if position == self.cursor_pos:
                    row = ["[", f"{initiative}", f"{name}", "]"]
                else:
                    row = ["", str(initiative), name, ""]
                table.add_row(row)

            output = table.draw()
        else:
            output = "Empty initiative queue."

        print()
        print(output)
        print()


def main():
    """Create a rfi.Repl instance and run it."""
    Repl().run()


if __name__ == "__main__":
    main()
