#!/usr/bin/env python3
"""RFI repl and main logic."""

from inspect import cleandoc

from dice import DiceException, roll
from prompt_toolkit import Application
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.utils import test_callable_args
from prompt_toolkit.widgets import CompletionsToolbar, TextArea
from texttable import Texttable

from . import __version__ as rfi_version  # pylint: disable=cyclic-import
from .initiative import InitiativeQueue


def _dice_roll_sum(dice_expr: str):
    try:
        result = roll(dice_expr)
    except DiceException:
        raise ValueError(f"Invalid dice expression: {dice_expr}")

    try:
        return sum(result)
    except TypeError:
        return result


class Repl(Application):
    # pylint: disable=no-self-use
    """REPL for RFI."""

    commands_usage = {
        "help": "help [command]",
        "add": "add {name} {init_expr}",
        "remove": "remove {name}",
        "show": "show",
        "start": "start",
        "reset": "reset",
        "removeall": "removeall",
        "next": "next",
        "prev": "prev",
        "chname": "chname {current_name} {new_name}",
        "chinit": "chinit {name} {init_expr}",
        "move": "move {name} (up|down)",
        "version": "version",
        "quit": "quit",
    }
    commands = list(commands_usage.keys())

    def __init__(self):
        """See help(Repl) for more information."""
        self.input_field, self.output_area = self._create_text_areas()
        layout = self._create_layout()
        keybindings = self._create_keybindings()
        super().__init__(layout=layout, full_screen=True, key_bindings=keybindings)
        self.queue = InitiativeQueue()
        self.cursor_pos = None
        self.output_area.text = self._get_intro_message()

    def _create_keybindings(self):
        keybindings = KeyBindings()

        @keybindings.add("up")
        def _scroll_up(_event):
            self.output_area.window._scroll_up()  # pylint: disable=protected-access

        @keybindings.add("down")
        def _scroll_down(_event):
            self.output_area.window._scroll_down()  # pylint: disable=protected-access

        return keybindings

    def _get_intro_message(self):
        text = f"\nrfi version {rfi_version}\n"
        text += "Type help to list available commands.\n"
        text += "\n"
        text += "Roll for initiative!"
        return text

    def _create_text_areas(self):
        completer = WordCompleter(self.commands, sentence=True)
        input_field = TextArea(
            height=1,
            prompt="> ",
            multiline=False,
            wrap_lines=False,
            completer=completer,
            accept_handler=self._accept_input,
        )
        output_area = TextArea(read_only=True, focusable=False, wrap_lines=False, scrollbar=True)
        return input_field, output_area

    def _create_layout(self):
        split = Window(char="-", height=1)
        container = HSplit([self.output_area, CompletionsToolbar(), split, self.input_field])
        return Layout(container, focused_element=self.input_field)

    def _accept_input(self, _buffer):
        user_input = self.input_field.text
        self.output_area.text = "\n" + self.parse(user_input)

    def parse(self, user_input):
        """Parse a user input string, and return the corresponding output."""
        try:
            cmd, *cmd_args = user_input.split()
        except ValueError:
            # Empty input, translate to "next"
            cmd, cmd_args = "next", []

        try:
            cmd_function = self._get_command_function(cmd)
        except AttributeError:
            return f"Unknown command: {cmd}."

        if not test_callable_args(cmd_function, cmd_args):
            return f"""
            Invalid usage of {cmd}.
            Expected usage: {self.commands_usage[cmd]}
            Type help {cmd} for more information.
            """

        try:
            return cmd_function(*cmd_args)
        except (ValueError, RuntimeError) as err:
            return f"Error: {err}"

        return ""

    def cmd_help(self, cmd: str = None):
        """
        Display help for one or all commands.

        Arguments:
            cmd (optional): command to get help on.
                If ommitted, show overview of all commands.

        Examples:
            help
            help add
            help help

        """
        if cmd is None:
            return self._help_all()
        else:
            return self._help_single(cmd)

    def cmd_add(self, name: str, init_expr: str):
        """
        Add entry to initiative order.

        Arguments:
            name: new entry name.
            init_expr: dice expression to calculate initiative; can be a constant.

        Examples:
            add Buzz 1d20+1
            add Explictica 15

        """
        initiative = _dice_roll_sum(init_expr)
        self.queue.add(name, initiative)
        try:
            if self.queue.position_of(name) <= self.cursor_pos:
                self._move_cursor(+1)
        except TypeError:
            pass
        return self._show_queue()

    def cmd_remove(self, name: str):
        """
        Remove an entry from initiative order.

        Arguments:
            name: name of entry to be removed.

        Examples:
            remove Elyn

        """
        try:
            if self.queue.position_of(name) < self.cursor_pos:
                self._move_cursor(-1)
        except TypeError:
            pass
        self.queue.remove(name)
        self._fix_cursor()
        return self._show_queue()

    def cmd_chname(self, current_name: str, new_name: str):
        """
        Rename an existing entry.

        Arguments:
            current_name: current name of entry to be updated.
            new_name: desired name of entry.

        Examples:
            rename Monster1 Troglodyte

        """
        self.queue.update_name(current_name, new_name)
        return self._show_queue()

    def cmd_chinit(self, name: str, init_expr: str):
        """
        Reassign initiative to an existing entry.

        Arguments:
            name: name of entry to be updated.
            init_expr: dice expression to calculate initiative; can be a constant.

        Examples:
            chinit Monter1 14
            chinit Tasha 1d20+3

        """
        new_initiative = _dice_roll_sum(init_expr)
        self.queue.update(name, new_initiative)
        return self._show_queue()

    def cmd_start(self):
        """Initialize the cursor, pointing it to the first entry in initiative order."""
        self.cursor_pos = 0
        return self._show_queue()

    def cmd_next(self):
        """Advance cursor to the next entry."""
        try:
            self._move_cursor(+1)
            return self._show_queue()
        except TypeError:
            raise RuntimeError("Attempt to move cursor before call to start")

    def cmd_prev(self):
        """Move cursor prev one position."""
        try:
            self._move_cursor(-1)
            return self._show_queue()
        except TypeError:
            raise RuntimeError("Attempt to move cursor before call to start")

    def cmd_move(self, name: str, direction: str):
        """
        Reorder entries with tied initiative, moving one of them up or down.

        Only to be used on entries whose initiative is tied with another's.

        Example:
            move Elyn up
            move Buzz up
            move Isis down

        """
        if direction == "up":
            self.queue.move_up(name)
            return self._show_queue()
        elif direction == "down":
            self.queue.move_down(name)
            return self._show_queue()
        else:
            raise ValueError("Direction must be up or down")

    def cmd_removeall(self):
        """Remove all entries of initiative queue."""
        self.queue.clear()
        self._fix_cursor()
        return self._show_queue()

    def cmd_reset(self):
        """Reset cursor to top of initiative queue."""
        if self.cursor_pos is None:
            raise RuntimeError("Nothing to reset, start was not used.")

        self.cursor_pos = 0
        self._fix_cursor()
        return self._show_queue()

    def cmd_show(self):
        """Show current state of initiative queue."""
        return self._show_queue()

    def cmd_quit(self):
        """Quit REPL."""
        self.exit()
        return ""

    def cmd_version(self):
        """Show version information."""
        return f"rfi version {rfi_version}"

    def _make_table(self):
        table = Texttable()
        screen_size = self.output.get_size()
        table.set_max_width(min(90, screen_size.columns))
        return table

    def _get_command_function(self, cmd: str):
        return getattr(self, f"cmd_{cmd}")

    def _help_all(self):
        table = self._make_table()
        table.set_deco(Texttable.HEADER | Texttable.VLINES)
        table.header(["Command", "Description", "Usage"])
        table.set_cols_align("lcl")
        for cmd, cmd_usage in self.commands_usage.items():
            cmd_help = self._get_cmd_short_help(cmd)
            if cmd_help is not None:
                table.add_row([cmd, cmd_help, cmd_usage])

        text = ""
        text += "Try help help for more information.\n"
        text += "Use the up and down arrows to scroll.\n\n"
        text += table.draw()
        text += "\n"
        text += "Use help {command} for more information about a specific command."
        return text

    def _help_single(self, cmd: str):
        cmd_help = self._get_cmd_full_help(cmd)
        if cmd_help is None:
            raise ValueError(f"No help available for command {cmd}")
        return cmd_help

    def _get_cmd_short_help(self, cmd: str):
        try:
            full_help = self._get_cmd_full_help(cmd)
            return full_help.split("\n", maxsplit=1)[0]
        except AttributeError:
            return None

    def _get_cmd_full_help(self, cmd: str):
        try:
            return cleandoc(self._get_command_function(cmd).__doc__)
        except AttributeError:
            return None

    def _move_cursor(self, delta: int):
        self.cursor_pos += delta + len(self.queue)
        self._fix_cursor()

    def _fix_cursor(self):
        if self.cursor_pos is None:
            # Nothing to fix
            return

        try:
            self.cursor_pos %= len(self.queue)
        except ZeroDivisionError:
            # This happens when calling % len and the queue is empty,
            # therefore we can set the cursor to None
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

        return output


def repl():
    """Create a Repl instance and run it."""
    Repl().run()


if __name__ == "__main__":
    repl()
