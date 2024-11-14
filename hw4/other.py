# from rotor import Rotor
# from reflector import Reflector
# from plugboard import Plugboard
# from machine import Enigma
# from plugboard import Cable
# from unittest.mock import patch
# from io import StringIO
# import sys
# from string import ascii_uppercase
# import pytest


# @pytest.fixture
# def setup():
#     return Enigma(key="AAA", cables=[('A', 'B'), ('C', 'D')], rotor_order=['I', 'II', 'III'])


# """Tests for __repr__"""

# def test_repr(setup):
#     expected = f"Keyboard <-> Plugboard <-> Rotor [{setup.r_rotor}] <-> Rotor [{setup.m_rotor}] <-> Rotor [{setup.l_rotor}] <-> Reflector"
#     assert expected == repr(setup)


# """Tests for Encipher and Decipher"""

# def test_decipher():
#     enigma_encode = Enigma()
#     enigma_decode = Enigma()
#     original_message = "HELLO WORLD"
#     enciphered_message = enigma_encode.encipher(original_message)
#     deciphered_message = enigma_decode.decipher(enciphered_message)
#     assert deciphered_message == original_message.replace(" ", "")


# """Tests for set_rotor_position"""

# def test_position_key_isalpha():
#     enigma = Enigma()
#     enigma.set_rotor_order(['I', 'II', 'III'])
#     with pytest.raises(ValueError) as excep_info:
#         enigma.set_rotor_position('123')
#     assert str(excep_info.value) == "Please provide a three letter position key such as AAA."


# def test_set_rotor_position_with_print(capsys):
#     enigma = Enigma()
#     enigma.set_rotor_order(['I', 'II', 'III'])
#     enigma.set_rotor_position("ABC", print_it=True)
#     captured = capsys.readouterr()
#     expected_output = "Rotor position successfully updated. Machine looks like\n"
#     assert expected_output in captured.out
#     assert str(enigma) in captured.out  


# """Tests for set_rotor_order"""

# def test_rotor_order_invalid_length():
#     enigma = Enigma()
#     with pytest.raises(ValueError) as excep_info:
#         enigma.set_rotor_order(['I', 'II'])
#     assert str(excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."
    
#     with pytest.raises(ValueError) as excep_info:
#         enigma.set_rotor_order(['I', 'II', 'III', 'V'])
#     assert str(excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."


# def test_rotor_order_invalid_names():
#     enigma = Enigma()
#     with pytest.raises(ValueError) as excep_info:
#         enigma.set_rotor_order(['I', 'II', 'X'])
#     assert str(excep_info.value) == "Rotor order must be a list of 3 strings from the set of preconfigured options I, II, III, or V. For example,  ['I', 'II', 'III']."


# def test_rotor_order_print():
#     enigma = Enigma()
#     rotor_order = ['I', 'II', 'III']
#     with patch('builtins.print') as mock_print:
#         enigma.set_rotor_order(rotor_order, print_it=True)
#         mock_print.assert_called_once() 
#         assert "Rotor order successfully updated. Machine looks like" in mock_print.call_args[0][0]


# """Tests for set_plugs"""

# def test_set_plugs_invalid_cable_format():
#     enigma = Enigma()
#     with pytest.raises(TypeError) as excinfo:
#         enigma.set_plugs([('A', 'B', 'C')])
#     assert str(excinfo.value) == "Please provide cables in the form of letter pairs like ('A', 'B')."


# def test_set_plugs_print():
#     enigma = Enigma()
#     cables = [('A', 'B'), ('C', 'D')]
#     captured_output = StringIO()
#     sys.stdout = captured_output
#     enigma.set_plugs(cables, print_it=True)
#     sys.stdout = sys.__stdout__
#     output = captured_output.getvalue()
#     assert "Plugboard successfully updated:" in output
#     assert str(enigma.plugboard) in output 


# """Tests for Constructor Errors and Special Cases"""

# @pytest.fixture
# def new_enigma():
#     return Enigma(key="AAA", cables=[('A', 'B'), ('C', 'D')], rotor_order=['I', 'II', 'III'])


# def test_invalid_constructor():
#     with pytest.raises(ValueError):
#         Enigma(key=None)

#     with pytest.raises(ValueError):
#         Enigma(key=123)

#     with pytest.raises(TypeError):
#         Enigma(cables=["wrong"])


# """Tests for Special Characters and State Preservation"""

# def test_special_characters():
#     enigma = Enigma()
#     enc1 = enigma.encipher("abc")
#     enc2 = enigma.encipher("ABC")
#     assert enc1 != enc2

#     with pytest.raises(ValueError):
#         enigma.encipher("A#C")


# def test_preserving_state():
#     enigma = Enigma()
#     initial_state = (
#         enigma.l_rotor._window,
#         enigma.m_rotor._window,
#         enigma.r_rotor._window,
#         enigma.plugboard._plugs.copy()
#     )
#     enigma.encipher("HELLO")
#     enigma.set_rotor_position("AAA")
#     reset_state = (
#         enigma.l_rotor._window,
#         enigma.m_rotor._window,
#         enigma.r_rotor._window,
#         enigma.plugboard._plugs.copy()
#     )
#     assert reset_state == initial_state


# """Tests for Rotor Position Edge Cases and Encoding/Decoding"""

# def test_rotor_position_edge_cases():
#     enigma = Enigma()
#     with pytest.raises(ValueError):
#         enigma.set_rotor_position("AA")

#     enigma.set_rotor_position("AAZ")
#     initial_middle = enigma.m_rotor._window
#     enigma.encode_decode_letter("A") 
#     assert enigma.m_rotor._window == initial_middle


# def test_encoding_decoding():
#     enigma = Enigma()
#     message = "RANDOMMESSAGE"
#     encoded_message = enigma.encipher(message)
#     enigma = Enigma()
#     decoded_message = enigma.encipher(encoded_message)
#     assert decoded_message == message











