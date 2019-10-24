"""RFI repl and main logic."""
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter


class Repl:  # pylint: disable=too-few-public-methods
    """REPL for RFI."""

    def __init__(self):
        """See help(Repl) for more information."""
        completer = WordCompleter(["add", "remove", "chname", "chroll"])
        self.session = PromptSession("> ", completer=completer)

    def run(self):
        """Run the REPL until EOF is reached."""
        while True:
            try:
                user_input = self.session.prompt()
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            else:
                print(user_input)


if __name__ == "__main__":
    Repl().run()
