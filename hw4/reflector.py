class Reflector:
    """
    This class defines the reflector for the Engima machine.
    """

    def __init__(self) -> None:
        # Note: this is the wiring for Reflector B of the Wehrmaht Engima.
        self._wiring = {
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

    def reflect(self, letter: str) -> str:
        """
        Given an input letter, return the reflected letter.
        """
        return self._wiring[letter]

    def __repr__(self) -> str:
        return f"Reflector wiring: \n{self._wiring}"