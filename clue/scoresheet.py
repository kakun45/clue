import clue
from typing import List



class Scoresheet:
    def __init__(self, players_names: List[str]):
        pass

    def is_valid(self) -> bool:
        """
        Checks validity.  For example, if two Room cards are both marked as ANSWER,
        that is invalid.  Or if two people have the same card, that is invalid.

        @returns true if the data structure is valid
        """
        pass  # TODO write unit tests

    def set_ownership(self, player: str, card: str, state: int) -> None:
        """
        Sets the "ownership" value for that player and card.

        :player: which player
        :card: which card
        :state: the value for the ownership state:  BLANK, HAS_CARD, DOESNT_HAVE_CARD

        example:  set_ownership("Olivia", MUSTARD, HAS_CARD)
        """
        pass

    def get_ownership(self, player: str, card: str) -> int:
        """
        Gets the "ownership" value for that player and card
        """
        pass

    def is_excluded(self, card: str) -> bool:
        pass

    def is_answer(self, card: str) -> bool:
        pass

    def print_scoresheet(self):
        """
        SUSPECTS    | P1| P2| P3|
        ----------------------------
        (Mustard)   | 0 | 0 | 0 |
        Green       | 0 | 0 |   |
        --Plum------| 0 |   |   |
        Peacock     | 0 | 0 | 1 |


        WEAPONS      | P1| P2| P3|
        ----------------------------
        --Knife------| 1 | 0 | 0 |
        Candlestick  | 0 | 0 |   |

        ROOMS        | P1| P2| P3|
        ----------------------------
        --Kitchen----| 1 | 0 | 0 |
        (Gazebo)     | 0 | 0 | 0 |
        """
        pass

    def __str__(self):
        return str(clue.ROOMS)