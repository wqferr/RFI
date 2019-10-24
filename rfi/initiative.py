# TODO docstrings

from bisect import bisect_left, bisect_right


class InitiativeQueue:
    def __init__(self):
        # This split is necessary due to how bisect works.
        # There is no key function, and creating a new list every time would be
        # unnecessary.
        self.names = []
        self.initiatives = []

    def add(self, name, initiative):
        if name in self.names:
            raise ValueError("Duplicate name in initiative queue.")

        insertion_idx = bisect_left(self.initiatives, initiative)
        self._add(name, initiative, insertion_idx)

    def remove(self, name):
        removal_idx = self._get_position(name)
        self._remove(removal_idx)

    def move_up(self, name):
        original_idx = self._get_position(name)
        initiative = self.initiatives[original_idx]
        max_valid_idx = bisect_right(self.initiatives, initiative) - 1

        if max_valid_idx > original_idx:
            self._move(original_idx, original_idx + 1)
        else:
            raise ValueError(f"Can't move {name} up without violating initiative order.")

    def move_down(self, name):
        original_idx = self._get_position(name)
        initiative = self.initiatives[original_idx]
        min_valid_idx = bisect_left(self.initiatives, initiative)

        if min_valid_idx < original_idx:
            self._move(original_idx, original_idx - 1)
        else:
            raise ValueError(f"Can't move {name} down without violating initiative order.")

    def _get_position(self, name):
        try:
            return self.names.index(name)
        except ValueError:
            raise ValueError(f"Name not in initiative queue: {name}")

    def _add(self, name, initiative, idx):
        self.names.insert(idx, name)
        self.initiatives.insert(idx, initiative)

    def _remove(self, idx):
        name, initiative = self.names[idx], self.initiatives[idx]
        del self.names[idx]
        del self.initiatives[idx]
        return name, initiative

    def _move(self, original_idx, final_idx):
        name, initiative = self._remove(original_idx)
        self._add(name, initiative, final_idx)

    def __iter__(self):
        max_idx = len(self)
        for idx in range(max_idx):
            yield self[idx]

    def __len__(self):
        return len(self.names)

    def __getitem__(self, idx):
        ordered_idx = -idx - 1
        return self.names[ordered_idx], self.initiatives[ordered_idx]
