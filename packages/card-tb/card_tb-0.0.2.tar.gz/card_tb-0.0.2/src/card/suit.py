# imports dataclass which is used to create datatypes for dice and state
from dataclasses import dataclass


HEARTS   = "HEARTS"
CLUBS    = "CLUBS"
SPADES   = "SPADES"
DIAMONDS = "DIAMONDS"

SUITS = [HEARTS, CLUBS, SPADES, DIAMONDS]

HEARTS_STRING   = "H"
CLUBS_STRING    = "C"
SPADES_STRING   = "S"
DIAMONDS_STRING = "D"

SUITS_STRING = [HEARTS_STRING, CLUBS_STRING, SPADES_STRING, DIAMONDS_STRING]


@dataclass
class Suit:
    value: str


    def __post_init__(self):
        if type(self.value) == str:
            
            if self.value in SUITS:
                pass

            else:
                raise ValueError()

        else:
            raise TypeError()


    @classmethod
    def string_to_suit(cls, suit_string: str):
        if type(suit_string) == str:

            if suit_string == HEARTS_STRING:
                return Suit(HEARTS)

            elif suit_string == CLUBS_STRING:
                return Suit(CLUBS)

            elif suit_string == SPADES_STRING:
                return Suit(SPADES)

            elif suit_string == DIAMONDS_STRING:
                return Suit(DIAMONDS)

            else:
                raise ValueError()

        else:
            TypeError()


    @classmethod
    def suit_to_string(cls, suit):
        if type(suit) == Suit:

            if suit.value == HEARTS:
                return HEARTS_STRING

            elif suit.value == CLUBS:
                return CLUBS_STRING

            elif suit.value == SPADES:
                return SPADES_STRING

            elif suit.value == DIAMONDS:
                return DIAMONDS_STRING

            else:
                raise ValueError()
                
        else:
            TypeError()


    def __str__(self):
        return Suit.suit_to_string(self)


def test():
    
    for i in range(len(SUITS)):
        suit = SUITS[i]
        suit_string = SUITS_STRING[i]

        s = Suit(suit)

        print(suit)
        print(s.value == suit)

        # str test
        print(str(s) == suit_string)

        # suit_to_string test and string_to_suit
        print(s.value == Suit.string_to_suit(Suit.suit_to_string(s)).value)
        print(suit_string == Suit.suit_to_string(Suit.string_to_suit(suit_string)))


if __name__ == "__main__":
    test()