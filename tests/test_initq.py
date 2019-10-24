"""Test InitiativeQueue behavior."""
import pytest

# pylint: disable=invalid-name
from rfi.initiative import InitiativeQueue


def test_insertion_no_ties():
    """Test insertion order without ties."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Elyn", 12)
    q.add("Explictica", 15)

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Explictica", 15)
    assert q[2] == ("Elyn", 12)


def test_double_insertion():
    """Test inserting the same name twice raising an error."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Elyn", 12)
    with pytest.raises(ValueError):
        q.add("Tasha", 15)


def test_list_conversion():
    """Test converting InitiativeQueue to a list."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Elyn", 12)
    q.add("Explictica", 15)

    expected_list = [("Tasha", 18), ("Explictica", 15), ("Elyn", 12)]
    assert list(q) == expected_list
