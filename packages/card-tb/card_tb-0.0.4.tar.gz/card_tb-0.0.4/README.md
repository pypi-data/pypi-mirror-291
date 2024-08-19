# Card Package

This is a simple card package which has the type card which is a suit, face. 

# Importing

You can import the card package by:
``` 
from card_tb import card
from card_tb import face
from card_tb import suit
```

# Uses
How you can use this package.

## Using card
How you can use card.

### Instantiate card.Card(suit: Suit, face: Face)
You can use the card using:
```
_card = card.Card(suit.Suit("KINGS"), face.Face("HEARTS"))
```
which has the values:
```
_card.suit.value
_card.face.value
```
of "KINGS", "HEARTS".

### card.Card.card_to_string(_card: card.Card)
A card can be converted to a string representation
```
card.Card.card_to_string(_card)
```
has the string representation of "H K".

### card.Card.string_to_card(string_representation_of_a_card: str)
The string representation can be converted to a card.

```
card_string = "H K"

card2 = Card.string_to_card(Card.card_to_string(card))
```
so card2 == card.Card(suit.Suit("HEARTS"), face.Face("KINGS")).


## Using suit
You can use suit:
```
s = suit.Suit("KINGS")
```
where you can access the value
```
s.value == "KINGS"
```
which has the constants
```
HEARTS   = "HEARTS"
CLUBS    = "CLUBS"
SPADES   = "SPADES"
DIAMONDS = "DIAMONDS"

SUITS = [HEARTS, CLUBS, SPADES, DIAMONDS]
```
and
```
HEARTS_STRING   = "H"
CLUBS_STRING    = "C"
SPADES_STRING   = "S"
DIAMONDS_STRING = "D"

SUITS_STRING = [HEARTS_STRING, CLUBS_STRING, SPADES_STRING, DIAMONDS_STRING]
```

```
suit.Suit.suit_to_string(s)
```
which gives "H".

```
suit.Suit.string_to_suit("H")
```
which gives ```suit("HEARTS")```.


## Using face
You can use face:
```
f = face.Face("HEARTS")
```
where you can access the value
```
f.value == "HEARTS"
```
which has the constants
```
ACES   = "ACES"
TWOS   = "TWOS"
THREES = "THREES"
FOURS  = "FOURS"
FIVES  = "FIVES"
SIXES  = "SIXES"
SEVENS = "SEVENS"
EIGHTS = "EIGHTS"
NINES  = "NINES"
TENS   = "TENS"
JACKS  = "JACKS"
QUEENS = "QUEENS"
KINGS  = "KINGS"

FACES = [ACES, TWOS, THREES, FOURS, FIVES, SIXES, SEVENS, EIGHTS, NINES, TENS, JACKS, QUEENS, KINGS]
```
and
```
ACES_STRING   = "A"
TWOS_STRING   = "2"
THREES_STRING = "3"
FOURS_STRING  = "4"
FIVES_STRING  = "5"
SIXES_STRING  = "6"
SEVENS_STRING = "7"
EIGHTS_STRING = "8"
NINES_STRING  = "9"
TENS_STRING   = "T"
JACKS_STRING  = "J"
QUEENS_STRING = "Q"
KINGS_STRING  = "K"

FACES_STRING = [ACES_STRING, TWOS_STRING, THREES_STRING, FOURS_STRING, FIVES_STRING, SIXES_STRING, SEVENS_STRING, EIGHTS_STRING, NINES_STRING, TENS_STRING, JACKS_STRING, QUEENS_STRING, KINGS_STRING]
```

```
face.Face.face_to_string(f)
```
which gives "K".

```
face.Face.string_to_face("K")
```
which gives ```face("KINGS")```.