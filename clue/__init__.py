from typing import List

# Card answer States  (whether the card is the answer or not...)
UNKNOWN = 0  # we dont know if a player has this card yet
EXCLUDED = 1  # we know that a player has this card, but we might not know which player
ANSWER = 2  # this was the murder weapon/suspect/room

# Ownership Info  (this is about the combination of a player and card, i.e. a single square on the scoresheet)
BLANK = 0  # NO info about this (player, card) yet. We don't know if the player has it or doesn't have it
HAS_CARD = 1
DOESNT_HAVE_CARD = 2


MUSTARD = "Mustard"
PLUM = "Plum"
GREEN = "Green"
PEACOCK = "Peacock"
SCARLET = "Scarlet"
WHITE = "White"
ROSE = "Rose"
GRAY = "Gray"
BRUNETTE = "Brunette"
PEACH = "Peach"

PEOPLE = [MUSTARD, PLUM, GREEN, PEACOCK, SCARLET, WHITE, ROSE, GRAY, BRUNETTE, PEACH]

KNIFE = "Knife"
CANDLESTICK = "Candlestick"
REVOLVER = "Revolver"
ROPE = "Rope"
PIPE = "Pipe"
WRENCH = "Wrench"
POISON = "Poison"
HORSESHOE = "Horseshoe"

WEAPONS = [KNIFE, CANDLESTICK, REVOLVER, ROPE, PIPE, WRENCH, POISON, HORSESHOE]

COURTYARD = "Courtyard"
GAZEBO = "Gazebo"
DRAWING = "Drawing Room"
DINING = "Dining Room"
KITCHEN = "Kitchen"
CARRIAGE = "Carriage House"
TROPHY = "Trophy Room"
CONSERVATORY = "Conservatory"
STUDIO = "Studio"
BILLIARD = "Billiard Room"
LIBRARY = "Library"
FOUNTAIN = "Fountain"

ROOMS = [COURTYARD, GAZEBO, DRAWING, DINING, KITCHEN, CARRIAGE, TROPHY, CONSERVATORY, STUDIO, BILLIARD, LIBRARY, FOUNTAIN]

ALL_CARDS = PEOPLE + WEAPONS + ROOMS


def longest_word(words: List[str]):
    longest = 0
    for item in words:  # card
        current = len(item)  # int
        if longest < current:  # ints
            longest = current
    return longest


def pad_right(word, min_length: int):
    """
    Adds spaces to the right of word to make it at least as long as the given length.
    :param word: the word to pad
    :param min_length: the minimum length to make the string
    :return: the string word, with spaces added to that it is at least `min_length` long
    """
    padding = min_length - len(word)
    return word + " " * padding  # " " * -1 --> "" (multiply by negative gives you empty string)


NORMAL_TEXT = "\033[0m"
LIGHT_GRAY = "\033[37m"
DARK_GRAY = "\033[90m"

INVERTED = "\033[7m"

# ANSWER_TEXT = "\033[41m"  # red highlight
ANSWER_TEXT = "\033[1m\033[91m"  # bold red
# ANSWER_TEXT = "\033[1m\033[93m"  # bold yellow

