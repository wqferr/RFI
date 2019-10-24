"""Test InitiativeQueue behavior."""

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
