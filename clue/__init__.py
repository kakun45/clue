# Card States  (whether the card is the answer or not...)
UNKNOWN = 0  # we dont know if a player has this card yet
EXCLUDED = 1  # some player has this card
ANSWER = 2  # this was the murder weapon/person/room

# Ownership Info  (this is about the combination of a player and card, i.e. a single square on the scoresheet)
BLANK = 0  # no info about this (player, card) yet
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

