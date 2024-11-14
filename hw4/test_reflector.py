from reflector import Reflector
import string
import pytest


@pytest.fixture
def expected_dict():
    return {
        "A": "Y",
        "B": "R",
        "C": "U",
        "D": "H",
        "E": "Q",
        "F": "S",
        "G": "L",
        "H": "D",
        "I": "P",
        "J": "X",
        "K": "N",
        "L": "G",
        "M": "O",
        "N": "K",
        "O": "M",
        "P": "I",
        "Q": "E",
        "R": "B",
        "S": "F",
        "T": "Z",
        "U": "C",
        "V": "W",
        "W": "V",
        "X": "J",
        "Y": "A",
        "Z": "T",
    }


def test_init(expected_dict):
    reflector = Reflector()
    assert reflector._wiring == expected_dict


def test_reflect(expected_dict):
    reflector = Reflector()
    for letter in string.ascii_uppercase:
        assert expected_dict[letter] == reflector.reflect(letter)


def test_repr(expected_dict):
    reflector = Reflector()
    expected_string = f"Reflector wiring: \n{expected_dict}"
    assert expected_string == repr(reflector)
