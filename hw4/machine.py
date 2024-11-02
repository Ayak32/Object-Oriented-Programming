#!/usr/bin/python

'''
Enigma Machine Simulation
Author: Emily Willson
Date: April 6, 2018
(Updated by Timothy Barron in 2024)

Details: This file holds the code necessary to actually run the Enigma machine simulation. It draws on the other component modules to provide the constituent parts of the machine and implements a command line interface to operate the encryption process.

Specifications: In particular, this module implements the 3 rotor Enigma machine with plugboard and reflector used by the German army during WWII.
'''

from string import ascii_uppercase

from rotor import Rotor
from reflector import Reflector
from plugboard import Cable, Plugboard

class Enigma():
    '''
    This class will bring together components to create an actual Enigma machine.

    Thought about geometrically, the Enigma can be viewed as follows:

    Keyboard -> Plugboard -> R Rotor -> M Rotor -> L Rotor -> Reflector.
    Lampboard <- Plugboard <- R Rotor <- M Rotor <- L Rotor <- Reflector.

    The generic initial rotor ordering (which can be changed by the user) is L = I, M = II, R = III (I,II,III are three Wehrmacht Enigma rotors with their configurations predefined in the Rotor class)
    '''

    def __init__(self, key='AAA', cables=None, rotor_order=['I', 'II', 'III']) -> None:
        '''
        Initializes the Enigma machine.

        key = Three letter string specifying the top/visible letter for the left, middle, and right rotors respectively. This determines indexing in the rotor.

        cables = Specifies which letters should be connected by cables in the plugboard. Cables can be passed in as a list of letter pairs like [('A', 'B'), ('C', 'D')] or a list of Cable objects like [Cable('A', 'B'), Cable('C', 'D')].

        rotor_order = Defines which rotor to set as the left, middle, and right rotors respectively when considering the Enigma geometrically as described above.
        '''
        # Set the key and rotor order.
        self.set_rotor_order(rotor_order)
        self.set_rotor_position(key)

        self.reflector = Reflector()
        self.plugboard = Plugboard()
        if cables is not None:
            self.set_plugs(cables)

    def __repr__(self) -> str:
        " A nice representation of the layout of the full machine"
        return f"Keyboard <-> Plugboard <-> Rotor [{self.r_rotor}] <-> Rotor [{self.m_rotor}] <-> Rotor [{self.l_rotor}] <-> Reflector"

    def encipher(self, message) -> str:
        """
        Given a message string, encode or decode that message.
        """
        cipher = []
        for letter in message.replace(" ", "").strip():
            cipher.append(self.encode_decode_letter(letter))
        return ''.join(cipher)

    def decipher(self, message) -> str:
        """
        Encryption == decryption.
        """
        return self.encipher(message)

    def encode_decode_letter(self, letter) -> str:
        """ Takes a letter as input, steps rotors accordingly, and returns letter output.
        Because Enigma is symmetrical, this works the same whether you encode or decode.
        """
        # Make sure the letter is in a-zA-Z.
        if not (len(letter) == 1 and letter.isalpha()):
            raise ValueError('Please provide a letter in a-zA-Z.')
        # First, go through plugboard.
        letter = self.plugboard.swap(letter.upper())
        # Next, step the rotors.
        self.r_rotor.step()
        # Send the letter through the rotors to the reflector.
        # Get the index of the letter that emerges from the rotor.
        left_pass = self.r_rotor.encode_letter(ascii_uppercase.index(letter), return_letter=True)
        # Pass letter back through the reflector.
        refl_output = self.reflector.reflect(left_pass)
        # Send the reflected letter back through the rotors.
        right_pass = self.l_rotor.encode_letter(ascii_uppercase.index(refl_output), forward=False, return_letter=True)
        # Finally, go back through the plugboard.
        final_letter = self.plugboard.swap(right_pass)
        return final_letter

    def set_rotor_position(self, position_key, print_it=False) -> None:
        '''
        Updates the visible window settings of the Enigma machine, rotating the rotors.
        The syntax for the rotor position key is three letter string of the form 'AAA' or 'ZEK'.
        The rotor order must be set before calling this method.
        '''
        if type(position_key)==str and len(position_key)==3:
            l_key = position_key[0]
            m_key = position_key[1]
            r_key = position_key[2]
        else:
            raise ValueError('Please provide a three letter position key such as AAA.')
        if not (l_key.isalpha() and m_key.isalpha() and r_key.isalpha()):
            raise ValueError('Please provide a three letter position key such as AAA.')
        self.l_rotor.change_setting(l_key)
        self.m_rotor.change_setting(m_key)
        self.r_rotor.change_setting(r_key)
        if print_it:
            print(f'Rotor position successfully updated. Machine looks like\n{self}')


    def set_rotor_order(self, rotor_order, print_it=False) -> None:
        '''
        Changes the order of rotors in the Engima machine to match that specified by the user.
        The syntax for the rotor order is a list of the form ['I', 'II', 'III'], where 'I' is the left rotor, 'II' is the middle rotor, and 'III' is the right rotor.
        '''
        if len(rotor_order) != 3 or not all([r in Rotor.PRECONFIGURED for r in rotor_order]):
            raise ValueError('Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  [\'I\', \'II\', \'III\'].')
        # Create the rotors
        self.l_rotor = Rotor.create_preconfigured_rotor(rotor_order[0])
        self.m_rotor = Rotor.create_preconfigured_rotor(rotor_order[1])
        self.r_rotor = Rotor.create_preconfigured_rotor(rotor_order[2])
        # Connect the rotors to each other
        self.m_rotor.connect_next(self.l_rotor)
        self.m_rotor.connect_previous(self.r_rotor)
        if print_it:
            print(f'Rotor order successfully updated. Machine looks like\n{self}')

    def set_plugs(self, cables, replace=False, print_it=False) -> None:
        '''
        Update the plugboard settings. Cables can be passed in as a list of letter pairs like [('A', 'B'), ('C', 'D')] or a list of Cable objects like [Cable('A', 'B'), Cable('C', 'D')].

        If replace is true, then this method will erase the current pluDboard settinDs and replace them with new ones.
        '''
        if replace:
            self.plugboard.remove_all_cables()
        for c in cables:
            if isinstance(c, tuple):
                if len(c) != 2 or not all([l.isalpha() for l in c]):
                    raise TypeError("Please provide cables in the form of letter pairs like ('A', 'B').")
                c = Cable(c[0], c[1])
            if not isinstance(c, Cable):
                raise TypeError("Please provide cables as Cable objects or as letter pairs.")
            self.plugboard.add_cable(c)
        if print_it:
            print('Plugboard successfully updated:')
            print(self.plugboard)
