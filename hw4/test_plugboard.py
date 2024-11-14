from plugboard import Plugboard
from plugboard import Cable

import pytest


@pytest.fixture
def setup():
    cab1 = Cable("A", "B")
    cab2 = Cable("C", "D")

    new_plug = Plugboard([cab1, cab2])
    return new_plug


"""Tests for add_cable"""


def test_add_letter1(setup):
    new_cable = Cable("A", "Z")
    with pytest.raises(ValueError) as excep_info:
        setup.add_cable(new_cable)
    assert str(excep_info.value) == "The plug for A is already in use."


def test_add_letter2(setup):
    new_cable = Cable("Z", "B")
    with pytest.raises(ValueError) as excep_info:
        setup.add_cable(new_cable)
    assert str(excep_info.value) == "The plug for B is already in use."


def test_add_invalid_type(setup):
    with pytest.raises(AttributeError) as excep_info:
        setup.add_cable("A")  # Passing a string instead of a Cable object
    assert str(excep_info.value) == "'str' object has no attribute 'letter1'"


def test_add_invalid_type_int(setup):
    with pytest.raises(AttributeError) as excep_info:
        setup.add_cable(1)  # Passing a string instead of a Cable object
    assert str(excep_info.value) == "'int' object has no attribute 'letter1'"


# def test_add_invalid_cable(setup):
#      # Passing a number as the second plug letter
#     new_cable = Cable("A", 123)
#     with pytest.raises(TypeError) as excep_info:
#         setup.add_cable(new_cable)
#     assert str(excep_info.value) == "'in <string>' requires string as left operand, not int"


def test_add(setup):
    new_cable = Cable("Y", "Z")
    setup.add_cable(new_cable)
    assert setup._plugs[new_cable.letter1] == new_cable.letter2
    assert setup._plugs[new_cable.letter2] == new_cable.letter1
    assert new_cable in setup._cables


def test_add_duplicate_cables(setup):
    # Create a cable that would duplicate an existing connection
    duplicate_cable_1 = Cable("A", "B")
    duplicate_cable_2 = Cable("B", "A")

    # Test adding a cable that already exists (should raise ValueError)
    with pytest.raises(ValueError) as excep_info:
        setup.add_cable(duplicate_cable_1)
    assert str(excep_info.value) == "The plug for A is already in use."

    # Test adding a cable in reverse order (should also raise ValueError)
    with pytest.raises(ValueError) as excep_info:
        setup.add_cable(duplicate_cable_2)
    assert str(excep_info.value) == "The plug for B is already in use."


"""Test for remove_cable"""


def test_remove_nonexistent_cable(setup):
    non_existent_cable = Cable("X", "Y")

    # Ensure that removing a non-existent cable raises the expected ValueError
    with pytest.raises(ValueError):
        setup.remove_cable(non_existent_cable)  # Should raise ValueError

    # Assert that the plugboard is unchanged
    assert "X" not in setup._plugs
    assert "Y" not in setup._plugs
    assert non_existent_cable not in setup._cables


def test_remove(setup):
    to_be_removed = Cable("A", "B")
    setup.remove_cable(to_be_removed)
    assert "A" not in setup._plugs.keys()
    assert "B" not in setup._plugs.keys()
    assert Cable("A", "B") not in setup._cables


def test_add_remove_add(setup):
    cable = Cable("A", "B")
    setup.remove_cable(cable)
    assert "A" not in setup._plugs
    setup.add_cable(cable)
    assert setup._plugs["A"] == "B"


"""Tests for remove_all_cables"""


def test_remove_all_empty():
    new_plug = Plugboard()
    try:
        new_plug.remove_all_cables()
    except Exception as e:
        pytest.fail(f"An unexpected exception was raised: {e}")


def test_remove_all(setup):
    setup.remove_all_cables()
    assert len(setup._cables) == 0


def test_remove_all_cables_multiple(setup):
    setup.remove_all_cables()
    assert len(setup._cables) == 0
    setup.add_cable(Cable("A", "B"))
    setup.add_cable(Cable("C", "D"))
    setup.remove_all_cables()
    assert len(setup._cables) == 0


def test_remove_already_removed_cable(setup):
    cable = Cable("A", "B")
    setup.remove_cable(cable)  # Remove the cable first
    with pytest.raises(ValueError) as excep_info:
        setup.remove_cable(cable)  # Attempt to remove it again
    assert str(excep_info.value) == "list.remove(x): x not in list"


def test_remove_all_from_empty():
    new_plugboard = Plugboard()
    new_plugboard.remove_all_cables()
    assert len(new_plugboard._cables) == 0
    assert len(new_plugboard._plugs) == 0


"""Tests for __init__"""


def test_init_none():
    new_plugboard = Plugboard()
    assert new_plugboard._plugs == {}
    assert new_plugboard._cables == []


def test_init():
    cab1 = Cable("A", "B")
    cab2 = Cable("C", "D")
    cab3 = Cable("E", "F")
    cab_list = [cab1, cab2, cab3]
    new_plugboard = Plugboard(cab_list)
    for cab in cab_list:
        assert cab in new_plugboard._cables

    assert new_plugboard._plugs == {
        "A": "B",
        "B": "A",
        "C": "D",
        "D": "C",
        "E": "F",
        "F": "E"
    }


def test_init_empty_list():
    new_plugboard = Plugboard([])
    assert new_plugboard._plugs == {}
    assert new_plugboard._cables == []


"""Tests for swap"""


def test_swap_empty_board():
    new_plugboard = Plugboard()
    assert new_plugboard.swap("A") == "A"


def test_swap_none(setup):
    assert setup.swap("Z") == "Z"


def test_swap(setup):
    assert setup.swap("A") == "B"
    assert setup.swap("B") == "A"
    assert setup.swap("C") == "D"
    assert setup.swap("D") == "C"


def test_swap_non_letter(setup):
    assert setup.swap("1") == "1"
    assert setup.swap("!") == "!"


"""Test for __repr__"""


def test_repr(setup):
    # expected_string = "A<->B\nC<->D"
    # assert expected_string == repr(setup)
    output = repr(setup)
    assert "A<->B" in output  # "A<->B" should be in the repr string
    assert "C<->D" in output  # "C<->D" should be in the repr string


def test_repr_empty():
    empty_plugboard = Plugboard()
    assert repr(empty_plugboard) == ""


"""TESTS FOR CABLE"""

"""Tests for __init__"""


def test_init_lowercase():
    with pytest.raises(ValueError) as excep_info_A:
        Cable("A", "b")
    assert str(excep_info_A.value) == "Cable must connect two capital letters A-Z."

    with pytest.raises(ValueError) as excep_info_B:
        Cable("a", "B")
    assert str(excep_info_B.value) == "Cable must connect two capital letters A-Z."


def test_init_equal():
    with pytest.raises(ValueError) as excep_info:
        Cable("A", "A")
    assert str(excep_info.value) == "Cannot connect a plug to itself."


def test_init_swapped():
    new_cable = Cable("A", "B")
    assert new_cable.letter1 == "A"
    assert new_cable.letter2 == "B"


def test_init_valid():
    new_cable = Cable("A", "B")
    assert new_cable.letter1 == "A"
    assert new_cable.letter2 == "B"


def test_init_int():
    with pytest.raises(TypeError) as excep_info:
        Cable(123, "B")
    assert str(
        excep_info.value) == "'in <string>' requires string as left operand, not int"


def test_init_int_left():
    with pytest.raises(TypeError) as excep_info:
        Cable("B", 123)
    assert str(
        excep_info.value) == "'in <string>' requires string as left operand, not int"


def test_init_invalid_character():
    with pytest.raises(ValueError) as excep_info:
        Cable("A", "1")  # Invalid character (numeric)
    assert str(excep_info.value) == "Cable must connect two capital letters A-Z."

    with pytest.raises(ValueError) as excep_info:
        Cable("A", "!")  # Invalid character (special character)
    assert str(excep_info.value) == "Cable must connect two capital letters A-Z."


"""Tests for __eq__"""


def test_eq_exact():
    cab1 = Cable("A", "B")
    cab2 = Cable("A", "B")
    assert cab1 == cab2


def test_eq_reverse():
    cab1 = Cable("A", "B")
    cab2 = Cable("B", "A")
    assert cab1 == cab2


def test_eq_neither():
    cab1 = Cable("A", "B")
    cab2 = Cable("C", "D")
    assert cab1 != cab2


def test_eq_edge_case_str():
    # Ensuring that comparing with a non-Cable object returns False
    cab = Cable("A", "B")
    with pytest.raises(AttributeError) as excep_info:
        cab != "random str"
    assert str(excep_info.value) == "'str' object has no attribute 'letter1'"


def test_eq_edge_case_int():
    # Ensuring that comparing with a non-Cable object returns False
    cab = Cable("A", "B")
    with pytest.raises(AttributeError) as excep_info:
        cab != 1
    assert str(excep_info.value) == "'int' object has no attribute 'letter1'"


"""Tests for __repr__"""


def test_repr(setup):
    lines = []
    for c in setup._cables:
        lines.append(repr(c))

    output = "\n".join(lines)

    assert output == repr(setup)
