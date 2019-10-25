"""Initiative tracking logic."""
from bisect import bisect_left, bisect_right
from typing import Iterator, Tuple


class InitiativeQueue:
    """Initiative tracking queue.

    Its external interface resembles that of a list, supporting
    iteration and item accessing.

    This is effectively a priority queue, but is implemented with O(n)
    insertion, deletion and lookup. This is not supposed to be an efficient
    data structure, just one that is easy to use in the RFI REPL.

    See add, remove, move_up and move_down as the main functions.
    """

    def __init__(self):
        """See help(InitiativeQueue) for more information."""
        # This split is necessary due to how bisect works.
        # There is no key function, and creating a new list every time would be
        # unnecessary.
        self.names = []
        self.initiatives = []

    def add(self, name: str, initiative: int) -> None:
        """Add a name to the initiative queue.

        Arguments:
            name (str): name of the new entry.
            initiative (int): entry initiative, with higher values coming first.

        Raises:
            ValueError: if called with a name that is already in the queue.

        """
        if name in self.names:
            raise ValueError("Duplicate name in initiative queue.")

        insertion_idx = bisect_left(self.initiatives, initiative)
        self._add(name, initiative, insertion_idx)

    def remove(self, name: str) -> None:
        """Remove an entry from the queue.

        Arguments:
            name (str): name of entry to be removed.

        Raises:
            ValueError: if the name is not in the queue.

        """
        removal_idx = self._get_index(name)
        self._remove(removal_idx)

    def update(self, name: str, new_initiative: int) -> None:
        """Update the initiative of an entry.

        Equivalent to
            self.remove(name)
            self.add(name, new_initiative)

        Arguments:
            name (str): name of entry to be updated.
            new_initiative (int): new value for entry initiative.

        Raises:
            ValueError: if the name is not in the queue.

        """
        self.remove(name)
        self.add(name, new_initiative)

    def update_name(self, name: str, new_name: str) -> None:
        """Change the name of an entry.

        Argumnents:
            name (str): current name of entry to be updated.
            new_name (str): desired name of entry.

        Raises:
            ValueError: if the current name is not in the queue.
            ValueError: if the new name is already in the queue.

        """
        idx = self._get_index(name)
        if new_name in self.names:
            raise ValueError("Desired name already exists in queue.")
        self.names[idx] = new_name

    def move_up(self, name: str) -> None:
        """Move a name up (closer to index 0) in case of a tie.

        This is only to be used when two or more entries have the same
        initiative, but their relative order has to be changed.

        Arguments:
            name (str): name of entry to be moved.

        Raises:
            ValueError: if the name is not in the queue.
            ValueError: if moving the entry up would violate initiative order.

        """
        original_idx = self._get_index(name)
        initiative = self.initiatives[original_idx]
        max_valid_idx = bisect_right(self.initiatives, initiative) - 1

        if max_valid_idx > original_idx:
            self._move(original_idx, original_idx + 1)
        else:
            raise ValueError(f"Can't move {name} up without violating initiative order.")

    def move_down(self, name: str) -> None:
        """Move a name down (further from index 0) in case of a tie.

        This is only to be used when two or more entries have the same
        initiative, but their relative order has to be changed.

        Arguments:
            name (str): name of entry to be moved.

        Raises:
            ValueError: if the name is not in the queue.
            ValueError: if moving the entry down would violate initiative order.

        """
        original_idx = self._get_index(name)
        initiative = self.initiatives[original_idx]
        min_valid_idx = bisect_left(self.initiatives, initiative)

        if min_valid_idx < original_idx:
            self._move(original_idx, original_idx - 1)
        else:
            raise ValueError(f"Can't move {name} down without violating initiative order.")

    def position_of(self, name: str) -> int:
        """Find position of name in queue.

        Arguments:
            name (str): name of entry to be found.

        Raises:
            ValueError: if the name is not in the list.

        """
        idx = self._get_index(name)
        return len(self) - idx - 1

    def clear(self) -> None:
        """Clear queue entries."""
        self.names.clear()
        self.initiatives.clear()

    def _get_index(self, name: str) -> int:
        try:
            return self.names.index(name)
        except ValueError:
            raise ValueError(f"Name not in initiative queue: {name}")

    def _add(self, name: str, initiative: int, idx: int) -> None:
        self.names.insert(idx, name)
        self.initiatives.insert(idx, initiative)

    def _remove(self, idx: int) -> (str, int):
        name, initiative = self.names[idx], self.initiatives[idx]
        del self.names[idx]
        del self.initiatives[idx]
        return name, initiative

    def _move(self, original_idx: int, final_idx: int) -> None:
        name, initiative = self._remove(original_idx)
        self._add(name, initiative, final_idx)

    def __iter__(self) -> Iterator[Tuple[str, int]]:
        """Iterate over self[idx] without looping."""
        max_idx = len(self)
        for idx in range(max_idx):
            yield self[idx]

    def __len__(self) -> int:
        """Retrieve size of queue."""
        return len(self.names)

    def __contains__(self, name: str) -> bool:
        """Check if there is an entry with the given name."""
        return name in self.names

    def __bool__(self) -> bool:
        """Check if the queue has elements in it."""
        return bool(self.names)

    def __getitem__(self, n: int) -> (str, int):  # pylint: disable=invalid-name
        """Retrieve the entry with the nth greatest initiative.

        Arguments:
            n (int): position of the list to retrieve.

        Returns:
            name (str): entry name.
            initiative (int): entry initiative.

        """
        # Invert index so self[0] returns the item with greatest initiative.
        idx = -n - 1
        return self.names[idx], self.initiatives[idx]
