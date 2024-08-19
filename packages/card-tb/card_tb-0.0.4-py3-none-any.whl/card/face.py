# imports dataclass which is used to create datatypes for dice and state
from dataclasses import dataclass


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


@dataclass
class Face:
    value: str


    def __post_init__(self):
        if type(self.value) == str:
            
            if self.value in FACES:
                pass

            else:
                raise ValueError()

        else:
            raise TypeError()


    @classmethod
    def string_to_face(cls, face_string: str):
        if type(face_string) == str:

            if face_string == ACES_STRING:
                return Face(ACES)

            elif face_string == TWOS_STRING:
                return Face(TWOS)

            elif face_string == THREES_STRING:
                return Face(THREES)

            elif face_string == FOURS_STRING:
                return Face(FOURS)

            elif face_string == FIVES_STRING:
                return Face(FIVES)

            elif face_string == SIXES_STRING:
                return Face(SIXES)

            elif face_string == SEVENS_STRING:
                return Face(SEVENS)

            elif face_string == EIGHTS_STRING:
                return Face(EIGHTS)

            elif face_string == NINES_STRING:
                return Face(NINES)

            elif face_string == TENS_STRING:
                return Face(TENS)

            elif face_string == JACKS_STRING:
                return Face(JACKS)

            elif face_string == QUEENS_STRING:
                return Face(QUEENS)

            elif face_string == KINGS_STRING:
                return Face(KINGS)

            else:
                raise ValueError()
                    
        else:
            TypeError()


    @classmethod
    def face_to_string(cls, face):
        if type(face) == Face:

            if face.value == ACES:
                return ACES_STRING 

            elif face.value == TWOS: 
                return TWOS_STRING

            elif face.value == THREES:
                return THREES_STRING

            elif face.value == FOURS: 
                return FOURS_STRING

            elif face.value == FIVES: 
                return FIVES_STRING

            elif face.value == SIXES:
                return SIXES_STRING

            elif face.value == SEVENS: 
                return SEVENS_STRING

            elif face.value == EIGHTS: 
                return EIGHTS_STRING

            elif face.value == NINES:
                return NINES_STRING

            elif face.value == TENS:
                return TENS_STRING

            elif face.value == JACKS:
                return JACKS_STRING

            elif face.value == QUEENS:
                return QUEENS_STRING

            elif face.value == KINGS:
                return KINGS_STRING

            else:
                raise ValueError()
             
        else:
            TypeError()


    def __str__(self):
        return Face.face_to_string(self)


def test():
    for i in range(len(FACES)):
        face = FACES[i]
        face_string = FACES_STRING[i]
        f = Face(face)
        print(face)
        print(f.value == face)
        print(str(f) == face_string)
        print(f.value == Face.string_to_face(Face.face_to_string(f)).value)
        print(face_string == Face.face_to_string(Face.string_to_face(face_string)))


if __name__ == "__main__":
    test()
