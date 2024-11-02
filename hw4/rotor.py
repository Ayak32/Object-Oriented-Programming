from string import ascii_uppercase


class Rotor:
    """
    This class defines the rotors for the Engima machine.
    """

    # Wiring information is derived from users.telenet.be/d.rijmenants/en/enigmatech.htm#wiringtables.
    # The next left rotor will step when the specified letters are visible in the window for that rotor.
    PRECONFIGURED = {
        "I": {
            "forward": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
            "backward": "UWYGADFPVZBECKMTHXSLRINQOJ",
            "notch": "Q",  # Next rotor steps when I moves from Q -> R
        },
        "II": {
            "forward": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
            "backward": "AJPCZWRLFBDKOTYUQGENHXMIVS",
            "notch": "E",  # Next rotor steps when II moves from E -> F
        },
        "III": {
            "forward": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
            "backward": "TAGBPCSDQEUFVNZHYIXJWLRKOM",
            "notch": "V",  # Next rotor steps when III moves from V -> W
        },
        "V": {
            "forward": "VZBRGITYUPSDNHLXAWMJQOFECK",
            "backward": "QCYLXWENFTZOSMVJUDKGIARPHB",
            "notch": "Z",  # Next rotor steps when V moves from Z -> A
        }
    }

    def __init__(
        self, rotor_name, forward_wiring, backward_wiring, notch, window_letter="A"
    ) -> None:

        self._name = rotor_name
        self._wiring_forward = forward_wiring
        self._wiring_backward = backward_wiring
        self._notch = notch

        # This is the letter visible to the operator.
        # Defining this is akin to defining the initial setting of the machine.
        self.change_setting(window_letter)

        # Rotors need to be connected to each other in a Machine before use.
        self._next_rotor = None
        self._prev_rotor = None

    @staticmethod
    def create_preconfigured_rotor(rotor_name, window_letter="A") -> "Rotor":
        """
        Factory method to create a rotor from the preconfigured settings.
        """
        if rotor_name not in Rotor.PRECONFIGURED:
            raise ValueError(
                "Rotor number was not recognized. Pass in I, II, III, or V to create a preconfigured rotor."
            )
        rotor_info = Rotor.PRECONFIGURED[rotor_name]
        return Rotor(
            rotor_name,
            rotor_info["forward"],
            rotor_info["backward"],
            rotor_info["notch"],
            window_letter=window_letter,
        )

    def __repr__(self) -> str:
        "Identify the rotor by its name and show the letter currently visible in the window."

        return f"Name: {self._name}, Window: {self._window}"

    def step(self) -> None:
        """
        Steps the rotor.
        If a next rotor is specified, do the check to see if we've reached the notch,
        thus requiring that rotor to step.
        """
        if self._next_rotor and self._window == self._notch:
            self._next_rotor.step()
        # Doublestep midrotor if required
        elif (
            self._next_rotor
            and not self._prev_rotor
            and self._next_rotor._window == self._next_rotor._notch
        ):
            self._next_rotor.step()
        self._offset = (self._offset + 1) % 26
        self._window = ascii_uppercase[self._offset]

    def encode_letter(
        self, index: int, forward=True, return_letter=False, print_it=False
    ) -> str | int:
        """
        Takes in an index associated with an alphabetic character.
        Uses internal rotor wiring to determine the output letter and its index.

        NOTE: indexing here is done with respect to the window position of the rotor.
        The letter visible in the window is the 0th letter in the index.
        The index then increments up the alphabet from this letter.

        EXAMPLE: 'Z' in window, then Z=0, A=1, B=2, etc.  Input and output
        letters from a rotor follow the same indexing scheme.
        """
        # Make sure it's number and not a letter.
        if type(index) == str and len(index) == 1:
            index = ascii_uppercase.index(index.upper())
        if forward:
            wiring = self._wiring_forward
        else:
            wiring = self._wiring_backward
        # Check the wiring table and find the associated letter with this index.
        output_letter = wiring[(index + self._offset) % 26]
        # Determine output index associated with this letter based on wiring.
        output_index = (ascii_uppercase.index(output_letter) - self._offset) % 26
        if print_it:
            print(
                "Rotor "
                + self._name
                + ": input = "
                + ascii_uppercase[(self._offset + index) % 26]
                + ", output = "
                + output_letter
            )
        if self._next_rotor and forward:
            return self._next_rotor.encode_letter(
                output_index, forward, return_letter, print_it
            )
        elif self._prev_rotor and not forward:
            return self._prev_rotor.encode_letter(
                output_index, forward, return_letter, print_it
            )
        else:
            if return_letter:
                return ascii_uppercase[output_index]
            else:
                return output_index

    def change_setting(self, new_window_letter) -> None:
        """
        Allows the operator to define a new setting for this rotor.
        This changes the window letter therefore changing the setup of the rotor.
        """
        self._window = new_window_letter.upper()
        self._offset = ascii_uppercase.index(self._window)

    def connect_next(self, rotor) -> None:
        "Connect this rotor on the left side to the one passed in"
        self._next_rotor = rotor
        rotor._prev_rotor = self

    def connect_previous(self, rotor) -> None:
        "Connect this rotor on the right side to the one passed in"
        self._prev_rotor = rotor
        rotor._next_rotor = self