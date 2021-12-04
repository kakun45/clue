import collections
from typing import List

import clue
from clue import MUSTARD, PLUM
from clue import BLANK, HAS_CARD, DOESNT_HAVE_CARD



class Scoresheet:
    def __init__(self, players_names: List[str]):
        if len(players_names) != len(set(players_names)):
            raise Exception(f"duplicate player names: {players_names}")

        # this MUST be an ordered list for printing to work
        self.players_names = [s.upper() for s in players_names]
        self.data = {}
        for card in clue.ALL_CARDS:
            self.data[card] = {}
            # self.data[PLUM] = {}
            for player in self.players_names:
                self.data[card][player] = clue.BLANK
        # self.answer_state = collections.defaultdict(lambda: clue.UNKNOWN)
        self.excluded = set()

    def is_valid(self) -> bool:
        """
        Checks validity.  For example, if two Room cards are both marked as ANSWER,
        that is invalid.  Or if two people have the same card, that is invalid.

        @returns true if the data structure is valid
        """
        # 1. more than one player cannot have the same card
        for card in clue.ALL_CARDS:
            count = 0
            for player in self.players_names:
                if self.get_ownership(player, card) == clue.HAS_CARD:  # 1
                    count += 1
            if count > 1:
                return False

        # 2. more than 1 card of the same group/type cannot be 'Answer'
        def _group_of_cards_check(group):
            count = 0
            for card in group:  # PLUM, 0
                if self.is_answer(card):  # DOESNT_HAVE_CARD = 2
                    count += 1
                if count > 1:
                    return False
            return True

        if not _group_of_cards_check(clue.PEOPLE):
            return False
        if not _group_of_cards_check(clue.WEAPONS):
            return False
        if not _group_of_cards_check(clue.ROOMS):
            return False

        # 3. Every card of the same type owned by someone
        def _excluded_check(group):
            count = 0
            for card in group:
                if self.is_excluded(card):
                    count += 1
                if count >= len(group):
                    return False
            return True

        if not _excluded_check(clue.PEOPLE):
            return False
        if not _excluded_check(clue.WEAPONS):
            return False
        if not _excluded_check(clue.ROOMS):
            return False

        # 4. A single player seems not to have any cards #todo?
        return True

    def set_ownership(self, player: str, card: str, state: int) -> None:
        """
        Sets the "ownership" value for that player and card. Set a checkmark or No-card for a single box.

        :player: which player
        :card: which card
        :state: the value for the ownership state:  BLANK, HAS_CARD, DOESNT_HAVE_CARD

        example:  set_ownership("Olivia", MUSTARD, HAS_CARD)
        """
        player = player.upper()
        if card not in clue.ALL_CARDS:
            raise ValueError(card)
        if player not in self.players_names:
            raise ValueError(player)
        #self.data.get(card, {}).get(player)  # 0
        self.data[card][player] = state

    def get_ownership(self, player: str, card: str) -> int:
        """
        returns a state
        Gets the "ownership" value for that player and card
        """
        player = player.upper()
        return self.data[card][player]

    # def set_card_answerstate(self, card: str, state: int) -> None:
    #     pass

    def set_excluded(self, card: str) -> None:
        """
        Call this method to record the fact that a card cannot be the answer (even though we
        might not know who has it)
        :param card:
        :return:
        """
        self.excluded.add(card)

    def is_excluded(self, card: str) -> bool:
        if card in self.excluded:
            return True
        else:
            # see if any player has it:
            for player in self.players_names:
                if self.data[card][player] == clue.HAS_CARD:
                    return True
            return False

    def is_answer(self, card: str) -> bool:
        """
        If we are certain no one has a card
        :param card:
        :return: True if Answer
        """
        for player in self.players_names:
            if self.data[card][player] != clue.DOESNT_HAVE_CARD:
                return False
        return True

    def print_scoresheet(self):
        """
        SUSPECTS    | P1| P2| P3|
        ---------------------------
        (Mustard)   | 0 | 0 | 0 |
        Green       | 0 | 0 |   |
        --Plum------| 0 |   |   |
        Peacock     | 0 | 0 | 1 |

        WEAPONS      | P1| P2| P3|
        ---------------------------
        --Knife------| 1 | 0 | 0 |
        Candlestick  | 0 | 0 |   |

        ROOMS        | P1| P2| P3|
        ---------------------------
        --Kitchen----| 1 | 0 | 0 |
        (Gazebo)     | 0 | 0 | 0 |
        """
        titles = {"SUSPECTS": clue.PEOPLE, "WEAPONS": clue.WEAPONS, "ROOMS": clue.ROOMS}
        short_names = [s[:3] for s in self.players_names]  # HAS THE SAME ORDER AS self.players_names

        for key in titles:
            print("")
            print(clue.pad_right(key, clue.longest_word(clue.ALL_CARDS)), "|", end="")
            for player in short_names:  # short names horizontally:  Dav|Oli|Xen|
                print(player, end="")
                print("|", end="")

            print("")
            print("----------------------------")
            for card in titles[key]:
                if self.is_excluded(card):
                    print(clue.LIGHT_GRAY, end="")
                elif self.is_answer(card):
                    print(clue.ANSWER_TEXT, end="")

                print(clue.pad_right(card, clue.longest_word(clue.ALL_CARDS)), "|", end="")
                for player in self.players_names:
                    print(self.box_str(self.get_ownership(player, card)), end="")
                    print("|", end="")
                print(clue.NORMAL_TEXT, end="")
                print("")


    @staticmethod
    def box_str(state: int) -> str:
        """
        Given the "ownership state" of a player and card, return the string that should be printed for that box
        :param state:
        :return:
        """
        # HAS_CARD -> " 1 "
        # DOESNT_HAVE_CARD -> " 0 "
        # BLANK -> "   "
        box = {BLANK: "   ", HAS_CARD: " 1 ", DOESNT_HAVE_CARD: " 0 "}
        return box[state]



    def __str__(self):
        return str(self.data)