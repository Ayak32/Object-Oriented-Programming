from rotor import Rotor
from string import ascii_uppercase
from unittest.mock import patch
from io import StringIO
import pytest


@pytest.fixture
def new_rotor():
    return Rotor("Rotor1", "ABC", "DEF", "T")


"""Tests for __init__"""


def test_init_no_window(new_rotor):
    assert new_rotor._name == "Rotor1"
    assert new_rotor._wiring_forward == "ABC"
    assert new_rotor._wiring_backward == "DEF"
    assert new_rotor._notch == "T"

    assert new_rotor._window == "A"
    assert new_rotor._offset == ascii_uppercase.index("A")

    assert new_rotor._next_rotor == None
    assert new_rotor._prev_rotor == None


def test_init_window():
    new_rotor = Rotor("Rotor1", "ABC", "DEF", "T", "z")
    assert new_rotor._name == "Rotor1"
    assert new_rotor._wiring_forward == "ABC"
    assert new_rotor._wiring_backward == "DEF"
    assert new_rotor._notch == "T"

    assert new_rotor._window == "Z"
    assert new_rotor._offset == ascii_uppercase.index("Z")

    assert new_rotor._next_rotor == None
    assert new_rotor._prev_rotor == None


"""Tests for create_preconfigured_rotor"""


def test_preconfigured_invalid_name():
    with pytest.raises(ValueError) as excep_info:
        Rotor.create_preconfigured_rotor("VI")
    assert str(excep_info.value) == "Rotor number was not recognized. Pass in I, II, III, or V to create a preconfigured rotor."


def test_preconfigured_valid():
    for name in Rotor.PRECONFIGURED:
        new_rotor = Rotor.create_preconfigured_rotor(name)
        rotor_info = Rotor.PRECONFIGURED[name]
        assert new_rotor._name == name
        assert new_rotor._wiring_forward == rotor_info["forward"]
        assert new_rotor._wiring_backward == rotor_info["backward"]
        assert new_rotor._notch == rotor_info["notch"]
        assert new_rotor._window == "A"
        assert new_rotor._offset == ascii_uppercase.index("A")
        assert new_rotor._next_rotor == None
        assert new_rotor._prev_rotor == None


def test_preconfigured_valid_window():
    for name in Rotor.PRECONFIGURED:
        new_rotor = Rotor.create_preconfigured_rotor(name, "Z")
        rotor_info = Rotor.PRECONFIGURED[name]
        assert new_rotor._name == name
        assert new_rotor._wiring_forward == rotor_info["forward"]
        assert new_rotor._wiring_backward == rotor_info["backward"]
        assert new_rotor._notch == rotor_info["notch"]
        assert new_rotor._window == "Z"
        assert new_rotor._offset == ascii_uppercase.index("Z")
        assert new_rotor._next_rotor == None
        assert new_rotor._prev_rotor == None


"""Tests for __repr__"""


def test_repr(new_rotor):
    assert repr(
        new_rotor) == f"Name: {new_rotor._name}, Window: {new_rotor._window}"


"""Tests for step"""


def test_step():
    rotor = Rotor.create_preconfigured_rotor("I")
    # next_rotor = Rotor.create_preconfigured_rotor("II")
    offset = rotor._offset
    window = rotor._window

    rotor.step()

    # Check that the rotor's offset has increased by 1
    assert rotor._offset == (offset + 1) % 26
    # Check that the rotor's window letter has changed correctly
    assert rotor._window == ascii_uppercase[(
        ascii_uppercase.index(window) + 1) % 26]


def test_step_notch():
    rotor = Rotor.create_preconfigured_rotor("I")
    next_rotor = Rotor.create_preconfigured_rotor("II")

    rotor.connect_next(next_rotor)

    # Moves the rotor to its notch position
    rotor.change_setting(rotor._notch)

    initial_next_rotor_offset = next_rotor._offset
    rotor.step()

    # The next rotor should have stepped
    assert next_rotor._offset == (initial_next_rotor_offset + 1) % 26


def test_double_step_modulo():
    rotor1 = Rotor.create_preconfigured_rotor("I")
    rotor2 = Rotor.create_preconfigured_rotor("II")

    # Connects the rotors
    rotor1.connect_next(rotor2)

    # Moves rotor2 to the step before its notch position
    rotor2.change_setting(
        ascii_uppercase[(ascii_uppercase.index(rotor2._notch) - 1) % 26])

    # Sets rotor2 at its notch to trigger the double-step
    rotor2.change_setting(rotor2._notch)

    # Steps rotor1, which should cause rotor2 to double-step
    rotor1.step()

    assert rotor2._offset == (ascii_uppercase.index(rotor2._notch) + 1) % 26


def test_double_step():
    rotor_1 = Rotor.create_preconfigured_rotor("III")
    rotor_2 = Rotor.create_preconfigured_rotor("II")
    rotor_3 = Rotor.create_preconfigured_rotor("I")

    rotor_1.connect_next(rotor_2)
    rotor_2.connect_next(rotor_3)

    rotor_1.change_setting("V")  # Rotor III at notch position V
    rotor_2.change_setting("D")

    rotor_1.step()
    assert rotor_1._window == "W"
    assert rotor_2._window == "E"


"""Tests for encode_letter"""


def test_encode_str():
    rotor = Rotor.create_preconfigured_rotor("I")
    try:
        rotor.encode_letter("A")
    except Exception as e:
        pytest.fail(f"encode_letter raised an exception: {e}")


def test_encode_forward():
    rotor = Rotor.create_preconfigured_rotor("I")
    index = ascii_uppercase.index("B")
    result = rotor.encode_letter(index, forward=True)
    expected = ascii_uppercase.index("K")
    assert result == expected


def test_encode_backward():
    rotor = Rotor.create_preconfigured_rotor("I")
    index = ascii_uppercase.index("K")
    result = rotor.encode_letter(index, forward=False)
    expected = ascii_uppercase.index("B")
    assert result == expected


def test_encode_letter_print():
    r = Rotor.create_preconfigured_rotor("I")
    with patch('sys.stdout', new=StringIO()) as mock_stdout:
        r.encode_letter(0, True, True, True)
        assert mock_stdout.getvalue()
        assert mock_stdout.getvalue() == "Rotor I: input = A, output = E\n"


def test_encode_return_letter():
    rotor = Rotor.create_preconfigured_rotor("I")
    index = ascii_uppercase.index("X")  # Test encoding letter 'X'
    result = rotor.encode_letter(index, forward=True, return_letter=True)
    expected = "R"  # Expected encoded letter
    assert result == expected


def test_encode_return_index():
    rotor1 = Rotor.create_preconfigured_rotor("I")
    rotor2 = Rotor.create_preconfigured_rotor("II")

    rotor1.connect_next(rotor2)

    rotor1.change_setting("A")
    rotor2.change_setting("B")

    index = ascii_uppercase.index("C")

    result = rotor1.encode_letter(index, forward=True)

    # The expected result is the encoding of 'C' through both rotors
    # Rotor I will map 'C' to 'K' (from wiring 'EKMFLGDQVZNTOWYHXUSPAIBRCJ')
    # Then Rotor II will map 'K' to the corresponding index
    # After passing through both rotors, the final letter should be 'R' (adjust based on the actual wiring)
    expected = ascii_uppercase.index("S")

    assert result == expected


def test_encode_letter_backward():

    rotor1 = Rotor.create_preconfigured_rotor("I")
    rotor2 = Rotor.create_preconfigured_rotor("II")

    rotor1.connect_previous(rotor2)

    rotor1.change_setting("A")
    rotor2.change_setting("B")

    index = ascii_uppercase.index("C")

    # Perform encoding through both rotors in reverse
    result = rotor1.encode_letter(index, forward=False, print_it=True)

    expected = 17

    assert result == expected


"""Tests for change_setting"""


def test_change_setting(new_rotor):
    new_rotor.change_setting("p")
    assert new_rotor._window == "p".upper()
    assert new_rotor._offset == ascii_uppercase.index("P")


"""Tests for connect_next"""


def test_connect_next():
    rotor1 = Rotor.create_preconfigured_rotor("I")
    rotor2 = Rotor.create_preconfigured_rotor("II")

    rotor1.connect_next(rotor2)
    assert rotor1._next_rotor == rotor2
    assert rotor2._prev_rotor == rotor1

    rotor2.connect_next(rotor1)
    assert rotor2._next_rotor == rotor1
    assert rotor1._prev_rotor == rotor2


def test_connect_next_same():
    rotor1 = Rotor.create_preconfigured_rotor("I")

    rotor1.connect_next(rotor1)
    assert rotor1._next_rotor == rotor1
    assert rotor1._prev_rotor == rotor1


"""Tests for connect_previous"""


def test_connect_previous():
    rotor1 = Rotor.create_preconfigured_rotor("I")
    rotor2 = Rotor.create_preconfigured_rotor("II")

    rotor1.connect_previous(rotor2)
    assert rotor1._prev_rotor == rotor2
    assert rotor2._next_rotor == rotor1

    rotor2.connect_previous(rotor1)
    assert rotor2._prev_rotor == rotor1
    assert rotor1._next_rotor == rotor2
