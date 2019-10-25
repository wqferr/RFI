"""Test InitiativeQueue behavior."""
import pytest

# pylint: disable=invalid-name
from rfi.initiative import InitiativeQueue


def test_item_accessing_no_ties():
    """Test insertion order without ties."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Elyn", 12)
    q.add("Explictica", 15)

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Explictica", 15)
    assert q[2] == ("Elyn", 12)

    assert q[-1] == ("Elyn", 12)
    assert q[-2] == ("Explictica", 15)
    assert q[-3] == ("Tasha", 18)


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


def test_insertion_with_ties():
    """Test stability of inserting a tied result."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 12)
    q.add("Explictica", 15)

    assert q[1] == ("Buzz", 15)
    assert q[-2] == ("Explictica", 15)


def test_move_up():
    """Test InitiativeQueue.move_up behavior and errors."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 15)
    q.add("Explictica", 15)
    q.add("Isis", 14)

    q.move_up("Elyn")
    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Elyn", 15)
    assert q[2] == ("Buzz", 15)
    assert q[3] == ("Explictica", 15)
    assert q[4] == ("Isis", 14)

    with pytest.raises(ValueError):
        q.move_up("Elyn")

    with pytest.raises(ValueError):
        q.move_up("Isis")

    with pytest.raises(ValueError):
        q.move_up("Tasha")

    with pytest.raises(ValueError):
        q.move_up("RandomName")

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Elyn", 15)
    assert q[2] == ("Buzz", 15)
    assert q[3] == ("Explictica", 15)
    assert q[4] == ("Isis", 14)


def test_move_down():
    """Test InitiativeQueue.move_down behavior and errors."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 15)
    q.add("Explictica", 15)
    q.add("Isis", 14)

    q.move_down("Elyn")
    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Buzz", 15)
    assert q[2] == ("Explictica", 15)
    assert q[3] == ("Elyn", 15)
    assert q[4] == ("Isis", 14)

    with pytest.raises(ValueError):
        q.move_down("Elyn")

    with pytest.raises(ValueError):
        q.move_down("Isis")

    with pytest.raises(ValueError):
        q.move_down("Tasha")

    with pytest.raises(ValueError):
        q.move_down("RandomName")

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Buzz", 15)
    assert q[2] == ("Explictica", 15)
    assert q[3] == ("Elyn", 15)
    assert q[4] == ("Isis", 14)


def test_remove():
    """Test removal for InitiativeQueue."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 17)
    q.add("Elyn", 16)
    q.add("Explictica", 15)
    q.add("Isis", 14)

    with pytest.raises(ValueError):
        q.remove("RandomName")

    assert q[1] == ("Buzz", 17)
    q.remove("Buzz")
    assert q[1] == ("Elyn", 16)

    assert q[-1] == ("Isis", 14)
    q.remove("Isis")
    assert q[-1] == ("Explictica", 15)

    assert q[0] == ("Tasha", 18)
    q.remove("Tasha")
    assert q[0] == ("Elyn", 16)
    q.remove("Elyn")
    assert q[0] == ("Explictica", 15)
    q.remove("Explictica")

    with pytest.raises(IndexError):
        _ = q[0]


def test_len():
    """Test len of InitiativeQueue."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 15)
    q.add("Explictica", 15)
    q.add("Isis", 14)

    assert len(q) == 5

    q.remove("Buzz")

    assert len(q) == 4


def test_update():
    """Test updating initiative."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 15)
    q.add("Explictica", 15)
    q.add("Isis", 14)

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Buzz", 15)
    assert q[2] == ("Elyn", 15)
    assert q[3] == ("Explictica", 15)
    assert q[4] == ("Isis", 14)

    q.update("Elyn", 16)

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Elyn", 16)
    assert q[2] == ("Buzz", 15)
    assert q[3] == ("Explictica", 15)
    assert q[4] == ("Isis", 14)

    with pytest.raises(ValueError):
        q.update("RandomName", 7)


def test_update_name():
    """Test name changing."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 15)
    q.add("Explictica", 15)
    q.add("Isis", 14)

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Buzz", 15)
    assert q[2] == ("Elyn", 15)
    assert q[3] == ("Explictica", 15)
    assert q[4] == ("Isis", 14)

    q.update_name("Explictica", "snek")

    assert q[0] == ("Tasha", 18)
    assert q[1] == ("Buzz", 15)
    assert q[2] == ("Elyn", 15)
    assert q[3] == ("snek", 15)
    assert q[4] == ("Isis", 14)

    with pytest.raises(ValueError):
        q.update_name("Elyn", "Isis")

    with pytest.raises(ValueError):
        q.update_name("RandomName", "OtherName")


def test_position_of():
    """Test position_of behavior."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 2)
    q.add("Explictica", 8)
    q.add("Isis", 17)

    assert q.position_of("Tasha") == 0
    assert q.position_of("Isis") == 1
    assert q.position_of("Buzz") == 2
    assert q.position_of("Explictica") == 3
    assert q.position_of("Elyn") == 4


def test_empty_check():
    """Test bool(q) behavior."""
    q = InitiativeQueue()
    assert not q

    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 2)

    assert bool(q)

    q.remove("Buzz")
    assert bool(q)

    q.remove("Elyn")
    assert bool(q)

    q.remove("Tasha")
    assert not q


def test_contingency():
    """Test 'name' in q behavior."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 2)
    q.add("Explictica", 8)
    q.add("Isis", 17)

    assert "Tasha" in q
    assert "Buzz" in q
    assert "Elyn" in q
    assert "Explictica" in q
    assert "Isis" in q

    assert "RandomName" not in q


def test_clear():
    """Test queue clearing."""
    q = InitiativeQueue()
    q.add("Tasha", 18)
    q.add("Buzz", 15)
    q.add("Elyn", 2)
    q.add("Explictica", 8)
    q.add("Isis", 17)

    assert bool(q)

    q.clear()

    assert not q
