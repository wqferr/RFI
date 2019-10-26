# Roll for Initiative!

## What is this?
This is a terminal-based initiative tracker primarily aimed at Dungeons & Dragons 5th edition.
I use the term "initiative" mostly for being recognizable, and most systems have something similar: a queue of actions
that happen in order given a numeric value.

## Motivation
All initiative trackers I found only are bloated. They cram as many features as possible with little to no regards to UX.
I'm going back to the basics: a CLI tool to manage initiative. No "create encounter". No "what is this creature's initiative bonus?" popup.

I hate the "create encounter" feature of these initiative trackers. I admit, this might be due to my GM style,
but I don't want to plan every single encounter the night before. I don't know what my players will do, I need the
flexibility to improvise.

The main motivation for me to create this, really, is just so I have a clean interface with really shallow menus
and **no setup time**. This is the project philosophy.

## Flow
### What do I do??
When in doubt, type `help` and press enter.

You can get help on a specific command by doing `help command`.

### Setting up
#### TL;DR
Run `add name initiative` as many times as you like. `initiative` may be a number or a diceroll expression.
