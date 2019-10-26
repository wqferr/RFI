# Roll for Initiative!

## What is this?
This is a terminal-based initiative tracker primarily aimed at Dungeons & Dragons 5th edition.
I use the term "initiative" mostly for being recognizable, and most systems have something similar: a queue of actions
that happen in order given a numeric value.

[Jump to installation instructions](#installation)

## Motivation
All initiative trackers I found only are bloated. They cram as many features as possible with little to no regards to UX.
I'm going back to the basics: a CLI tool to manage initiative. No "create encounter". No "what is this creature's initiative bonus?" popup.

I hate the "create encounter" feature of these initiative trackers. I admit, this might be due to my GM style,
but I don't want to plan every single encounter the night before. I don't know what my players will do, I need the
flexibility to improvise.

The main motivation for me to create this, really, is just so I have a clean interface with really shallow menus
and **no setup time**. This is the project philosophy.

## Quick tips
- Type `help` or `help command` if you have any doubts.
- Tab completion is your friend. After beginning to type a command, press tab to cycle through the suggestions.

## Flow
This is a TL;DR. You can find more information after this.
- Run `add name initiative` as many times as you like. `initiative` may be a number or a diceroll expression.
  - Entries are ordered by their decreasing initiative value.
  - If there is a tie, you can reorder them using `move lower_entry_name up` or `move upper_entry_name down`.
- Any time you want to see the queue but it's not visible, run `show`.
- Run `start`.
- Press enter when the input field is empty to advance to next entry.
- When a creature dies or for some other reason its entry is no longer relevant to the queue, type `remove dead_creature_name`.

That's pretty much what you need to know to use it at a basic level.

## Advanced usage
Todo

# Installation
To install the `rfi` command to your user scope, run:

```
pip install --user --upgrade roll-for-initiative
```

If you want to install directly from source, you can do:

```
cd /path/to/target/source/dir
git clone https://github.com/wqferr/RFI
cd RFI
pip install --user --upgrade flit
flit install -s
```

# Running it
After installing it with either method, you can run it with `rfi` on linux, or with `python -m rfi.app`
on any platform if that doesn't work.

# Special thanks
This application is made using the following libraries and tools:
- [flit](https://github.com/takluyver/flit) (build system)
- [pipenv](https://github.com/pypa/pipenv) (virtual environment)
- [texttable](https://github.com/foutaise/texttable/) (pretty text tables)
- [dice](https://github.com/borntyping/python-dice) (dice rolling for `add` and `chinit`)
