from rotor import Rotor
from reflector import Reflector
from plugboard import Plugboard
from machine import Enigma
from plugboard import Cable
from unittest.mock import patch
from io import StringIO
import sys
from string import ascii_uppercase
import pytest


@pytest.fixture
def setup():
    return Enigma(key="AAA", cables=[('A', 'B'), ('C', 'D')], rotor_order=['I', 'II', 'III'])


@pytest.fixture
def new_engima():
    return Enigma(key="AAA", cables=[('A', 'B'), ('C', 'D')], rotor_order=['I', 'II', 'III'])


"""Tests for init"""


def test_invalid_init():
    with pytest.raises(ValueError):
        Enigma(key=None)

    with pytest.raises(ValueError):
        Enigma(key=123)

    with pytest.raises(TypeError):
        Enigma(cables=["wrong"])

    enigma = Enigma()
    assert enigma.r_rotor._next_rotor._next_rotor == enigma.l_rotor
    assert enigma.l_rotor._prev_rotor._prev_rotor == enigma.r_rotor


"""Test for repr"""


def test_repr(setup):
    expected = f"Keyboard <-> Plugboard <-> Rotor [{setup.r_rotor}] <-> Rotor [{setup.m_rotor}] <-> Rotor [{setup.l_rotor}] <-> Reflector"
    assert expected == repr(setup)


"""Test for decipher"""


def test_decipher():
    # Initialize Enigma with a known configuration.
    enigma_encode = Enigma()
    enigma_decode = Enigma()

    # Define a message to encode and then decode
    original_message = "HELLO WORLD"

    # Encipher the message using the first Enigma instance
    enciphered_message = enigma_encode.encipher(original_message)

    # Decipher the enciphered message using a second Enigma instance with the same settings
    deciphered_message = enigma_decode.decipher(enciphered_message)

    # Assert that deciphering brings us back to the original message (without spaces)
    assert deciphered_message == original_message.replace(" ", "")


"""Test for encipher"""


def test_special_characters():
    enigma = Enigma()

    enc1 = enigma.encipher("abc")
    enc2 = enigma.encipher("ABC")
    assert enc1 != enc2

    with pytest.raises(ValueError):
        enigma.encipher("A#C")

    initial_state = (enigma.l_rotor._window,
                     enigma.m_rotor._window, enigma.r_rotor._window)
    enigma.encode_decode_letter("A")
    new_state = (enigma.l_rotor._window,
                 enigma.m_rotor._window, enigma.r_rotor._window)
    assert new_state != initial_state  # Rotors should have moved


"""Tests for set_rotor_position"""


def test_position_key_isalpha():
    enigma = Enigma()
    enigma.set_rotor_order(['I', 'II', 'III'])
    with pytest.raises(ValueError) as excep_info:
        enigma.set_rotor_position('123')
    assert str(
        excep_info.value) == "Please provide a three letter position key such as AAA."


def test_set_rotor_position_with_print(capsys):
    enigma = Enigma()

    # First, set the rotor order so the machine is ready to set the rotor position
    enigma.set_rotor_order(['I', 'II', 'III'])

    # Set rotor position with print_it=True
    enigma.set_rotor_position("ABC", print_it=True)

    # Capture the printed output
    captured = capsys.readouterr()

    # Expected output format (substitute this with the exact expected output if you have it)
    expected_output = "Rotor position successfully updated. Machine looks like\n"

    # Check if the expected output is in the captured output
    assert expected_output in captured.out
    # Ensure the Enigma machine's string representation is printed
    assert str(enigma) in captured.out


def test_rotor_position_edge_cases():
    enigma = Enigma()

    with pytest.raises(ValueError):
        enigma.set_rotor_position("AA")

    enigma.set_rotor_position("AAZ")
    initial_middle = enigma.m_rotor._window
    enigma.encode_decode_letter("A")
    assert enigma.m_rotor._window == initial_middle

    enigma.set_rotor_position("BCD")
    assert (enigma.l_rotor._window, enigma.m_rotor._window,
            enigma.r_rotor._window) == ("B", "C", "D")


"""Tests for set_rotor_order"""


def test_rotor_order_invalid_length():
    enigma = Enigma()

    # Test with fewer than 3 rotors
    with pytest.raises(ValueError) as excep_info:
        enigma.set_rotor_order(['I', 'II'])
    assert str(
        excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."
    # Test with more than 3 rotors
    with pytest.raises(ValueError) as excep_info:
        enigma.set_rotor_order(['I', 'II', 'III', 'V'])
    assert str(
        excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."


def test_rotor_order_invalid_names():
    enigma = Enigma()

    # Test with an invalid rotor name
    with pytest.raises(ValueError) as excep_info:
        # 'X' is not a valid rotor name
        enigma.set_rotor_order(['I', 'II', 'X'])
    assert str(
        excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."
    # Test with completely invalid rotor names
    with pytest.raises(ValueError) as excep_info:
        # None of these are valid rotors
        enigma.set_rotor_order(['A', 'B', 'C'])
    assert str(
        excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."

    with pytest.raises(ValueError) as excep_info:
        enigma.set_rotor_order([1, 2, 3])
    assert str(
        excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."


def test_rotor_order_print():
    e = Enigma()
    with patch('sys.stdout', new=StringIO()) as m_stdout:
        e.set_rotor_order(['I', 'I', 'I'], True)
        assert m_stdout.getvalue()
        expected_output = "Rotor [Name: I, Window: A] <-> Rotor [Name: I, Window: A] <-> Rotor [Name: I, Window: A]"
        assert expected_output in m_stdout.getvalue()


"""Tests for set_plugs"""


def test_set_plugs_invalid_cable_format():
    enigma = Enigma()

    # A cable that has more than two letters
    with pytest.raises(TypeError) as excinfo:
        enigma.set_plugs([('A', 'B', 'C')])
    assert str(
        excinfo.value) == "Please provide cables in the form of letter pairs like ('A', 'B')."

    # A cable that has only one letter
    with pytest.raises(TypeError) as excinfo:
        enigma.set_plugs([('A',)])
    assert str(
        excinfo.value) == "Please provide cables in the form of letter pairs like ('A', 'B')."

    # A cable that includes a non-alphabet character
    with pytest.raises(TypeError) as excinfo:
        enigma.set_plugs([('A', '1')])
    assert str(
        excinfo.value) == "Please provide cables in the form of letter pairs like ('A', 'B')."

    # A completely non-alphabetic cable
    with pytest.raises(TypeError) as excinfo:
        enigma.set_plugs([('1', '2')])
    assert str(
        excinfo.value) == "Please provide cables in the form of letter pairs like ('A', 'B')."


def test_set_plugs_print():
    enigma = Enigma()

    cables = [('A', 'B'), ('C', 'D')]

    captured_output = StringIO()
    sys.stdout = captured_output

    enigma.set_plugs(cables, print_it=True)

    sys.stdout = sys.__stdout__

    output = captured_output.getvalue()
    assert "Plugboard successfully updated:" in output
    assert str(enigma.plugboard) in output


def test_set_plugs_print_other():
    enigma = Enigma()
    enigma.set_plugs([('A', 'B'), ('C', 'D')])
    assert len(enigma.plugboard._cables) == 2
    assert enigma.plugboard._cables == [Cable('A', 'B'), Cable('C', 'D')]
    enigma.set_plugs([('E', 'F')], True)
    assert len(enigma.plugboard._cables) == 1
    assert enigma.plugboard._cables == [Cable('E', 'F')]

    with patch('sys.stdout', new=StringIO()) as mock_stdout:
        enigma.set_plugs([('G', 'H')], False, True)
        assert mock_stdout.getvalue()
        msg = "Plugboard successfully updated:"
        assert msg in mock_stdout.getvalue()


def test_plugboard_config():
    enigma = Enigma()

    # Test duplicate connections
    with pytest.raises(ValueError):
        enigma.set_plugs([("A", "B"), ("A", "C")])

    # Test self-connections
    with pytest.raises(ValueError):
        enigma.set_plugs([("A", "A")])

    # Test replacement behavior
    enigma = Enigma()
    enigma.set_plugs([("A", "B")])
    enigma.set_plugs([("C", "D")], replace=True)
    assert "A" not in enigma.plugboard._plugs

    # Test maximum connections
    max_cables = [Cable(chr(65+i), chr(90-i)) for i in range(13)]
    with pytest.raises(ValueError):
        enigma.set_plugs(max_cables)


"""Tests for encode_decode"""


def test_encode_decode_letter_invalid_input(setup):
    # Test with multiple characters
    with pytest.raises(ValueError) as exc_info:
        setup.encode_decode_letter("ab")
    assert str(exc_info.value) == "Please provide a letter in a-zA-Z."

    # Test with a number
    with pytest.raises(ValueError) as exc_info:
        setup.encode_decode_letter("1")
    assert str(exc_info.value) == "Please provide a letter in a-zA-Z."

    # Test with a special character
    with pytest.raises(ValueError) as exc_info:
        setup.encode_decode_letter("!")
    assert str(exc_info.value) == "Please provide a letter in a-zA-Z."

    # Test with an empty string
    with pytest.raises(ValueError) as exc_info:
        setup.encode_decode_letter("")
    assert str(exc_info.value) == "Please provide a letter in a-zA-Z."


def test_encoding_decoding():
    enigma = Enigma()
    message = "RANDOMMESSAGE"

    encoded_message = enigma.encipher(message)
    enigma = Enigma()  # Reset machine
    decoded_message = enigma.encipher(encoded_message)

    # Check if decoding restores the original message
    assert decoded_message == message
