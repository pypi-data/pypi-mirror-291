# imports random module for random number generation for random dice values
import random

# imports dataclass which is used to create datatypes for dice and state
from dataclasses import dataclass

# imports typing which are type annotations
from typing import Any
from typing import Union
from typing import List
from typing import Tuple

# imports copy which is used to deepcopy a value
import copy

import os
import sys

print(os.path.dirname(__file__))
#file_path = sys.path(str(__file__))
sys.path.append(os.path.dirname(__file__))

# imports suit which is used to store card suits
import suit as _suit
# from suit import Suit, SUITS, SUITS_STRING

# imports face which is used to store card faces
import face as _face
# from . import Face, FACES, FACES_STRING


@dataclass
class Card:
    suit: _suit.Suit
    face: _face.Face


    def __post_init__(self):
        if type(self.suit) == _suit.Suit:
            
            if type(self.face) == _face.Face:
                pass

            else:
                raise TypeError()

        else:
            raise TypeError()


    @classmethod
    def string_to_card(cls, card_string: str):
        if type(card_string) == str:
            suit_string, face_string = card_string.split()

            return Card(suit=_suit.Suit.string_to_suit(suit_string), face=_face.Face.string_to_face(face_string))

        else:
            TypeError()


    @classmethod
    def card_to_string(cls, card):
        if type(card) == Card:
            return str(card.suit) + " " + str(card.face)
                
        else:
            TypeError()


    def __str__(self):
        return Card.card_to_string(self) 


def test():
    for i in range(len(_face.FACES)):
        face = _face.FACES[i]
        face_string = _face.FACES_STRING[i]
        f = _face.Face(face)

        for j in range(len(_suit.SUITS)):
            suit = _suit.SUITS[j]
            suit_string = _suit.SUITS_STRING[j]
            s = _suit.Suit(suit)

            card = Card(s, f)
            card2 = Card.string_to_card(Card.card_to_string(card))

            print(card)
            print(card2.face.value == card.face.value and card2.suit.value == card.suit.value)
            print(Card.card_to_string(Card.string_to_card(str(card))) == str(card))
            print(card2.face.value == face and card2.suit.value == suit)


if __name__ == "__main__":
    test()      
