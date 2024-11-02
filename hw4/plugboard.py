
from string import ascii_uppercase

class Plugboard():
    '''
    This class defines the plugboard for the Engima machine.
    '''
    def __init__(self, cables=None) -> None:
        '''
        Initialize the plugboard.
        Input should be a list of Cable objects connecting two letters.
        '''
        self._plugs = {}
        if cables is None:
            cables = []
        self._cables = []
        for c in cables:
            self.add_cable(c)

    def swap(self, letter:str) -> str:
        '''
        Given a letter, return the swapped letter. If there is no cable connected to the letter, return the letter itself.
        '''
        swap = self._plugs.get(letter)
        if swap is None:
            return letter
        else:
            return swap

    def __repr__(self) -> str:
        '''
        A nice representation of swaps so the user can view the internal workings.
        '''
        lines = []
        for c in self._cables:
            lines.append(repr(c))
        return "\n".join(lines)
    
    def add_cable(self, cable) -> None:
        '''
        Add a cable to the plugboard.
        '''

        if cable.letter1 in self._plugs:
            raise ValueError(f"The plug for {cable.letter1} is already in use.")    
        if cable.letter2 in self._plugs:
            raise ValueError(f"The plug for {cable.letter2} is already in use.")
        self._plugs[cable.letter1] = cable.letter2
        self._plugs[cable.letter2] = cable.letter1
        self._cables.append(cable)

    def remove_cable(self, cable) -> None:
        '''
        Remove a cable from the plugboard.
        '''
        if cable.letter1 in self._plugs:
            del self._plugs[cable.letter1]
        if cable.letter2 in self._plugs:
            del self._plugs[cable.letter2]
        self._cables.remove(cable)


    def remove_all_cables(self) -> None:
        '''
        Remove all cables from the plugboard.
        '''
        while (len(self._cables) > 0):
            self.remove_cable(self._cables[0])
            



class Cable:
    '''
    This class defines cable connecting two plugs on the plugboard.
    '''
    def __init__(self, letter1, letter2) -> None:
        '''
        Initialize the plug.
        '''
        if letter1 not in ascii_uppercase or letter2 not in ascii_uppercase:
            raise ValueError("Cable must connect two capital letters A-Z.")
        if letter1 == letter2:
            raise ValueError("Cannot connect a plug to itself.")
        self.letter1 = letter1
        self.letter2 = letter2

    def __eq__(self, value) -> bool:
        '''
        Check if two cables are connecting the same plugs
        ''' 
        exact_match = self.letter1 == value.letter1 and self.letter2 == value.letter2
        reverse_match = self.letter1 == value.letter2 and self.letter2 == value.letter1
        return exact_match or reverse_match

    def __repr__(self) -> str:
        '''
        A nice representation of the cable so the user can view the internal workings.
        '''
        return f"{self.letter1}<->{self.letter2}"