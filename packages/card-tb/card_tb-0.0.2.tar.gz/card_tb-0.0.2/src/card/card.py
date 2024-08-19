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

# imports suit which is used to store card suits
from suit import Suit, SUITS, SUITS_STRING

# imports face which is used to store card faces
from face import Face, FACES, FACES_STRING


@dataclass
class Card:
    suit: Suit
    face: Face


    def __post_init__(self):
        if type(self.suit) == Suit:
            
            if type(self.face) == Face:
                pass

            else:
                raise TypeError()

        else:
            raise TypeError()


    @classmethod
    def string_to_card(cls, card_string: str):
        if type(card_string) == str:
            suit_string, face_string = card_string.split()

            return Card(suit=Suit.string_to_suit(suit_string), face=Face.string_to_face(face_string))

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
    for i in range(len(FACES)):
        face = FACES[i]
        face_string = FACES_STRING[i]
        f = Face(face)

        for j in range(len(SUITS)):
            suit = SUITS[j]
            suit_string = SUITS_STRING[j]
            s = Suit(suit)

            card = Card(s, f)
            card2 = Card.string_to_card(Card.card_to_string(card))

            print(card)
            print(card2.face.value == card.face.value and card2.suit.value == card.suit.value)
            print(Card.card_to_string(Card.string_to_card(str(card))) == str(card))
            print(card2.face.value == face and card2.suit.value == suit)


if __name__ == "__main__":
    test()      
