import collections
from typing import List

import clue
from clue import MUSTARD, PLUM
from clue import BLANK, HAS_CARD, DOESNT_HAVE_CARD, MASTER_DETECTIVE


class Scoresheet:
    def __init__(
        self,
        players_names: List[str],
        current_player: str,
        game: clue.Game = MASTER_DETECTIVE,
    ):
        if len(players_names) != len(set(players_names)):
            raise Exception(f"duplicate player names: {players_names}")

        # this MUST be an ordered list for printing to work
        self.players_names = [s.upper() for s in players_names]
        self.current_player = current_player
        self.game = game
        self.data = {}
        for card in game.all_cards:  # clue.ALL_CARDS:
            self.data[card] = {}
            # self.data[PLUM] = {}
            for player in self.players_names:
                self.data[card][player] = clue.BLANK
        # self.answer_state = collections.defaultdict(lambda: clue.UNKNOWN)
        self.excluded = set()

    def all_cards(self) -> List[str]:
        return self.game.all_cards

    def player_count(self) -> int:
        return len(self.players_names)

    def is_valid(self) -> bool:
        """
        Checks validity.  For example, if two Room cards are both marked as ANSWER,
        that is invalid.  Or if two people have the same card, that is invalid.

        @returns true if the data structure is valid
        """
        # 1. more than one player cannot have the same card
        for card in self.game.all_cards:
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

        if not _group_of_cards_check(self.game.suspects):
            return False
        if not _group_of_cards_check(self.game.weapons):
            return False
        if not _group_of_cards_check(self.game.rooms):
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

        if not _excluded_check(self.game.suspects):
            return False
        if not _excluded_check(self.game.weapons):
            return False
        if not _excluded_check(self.game.rooms):
            return False

        # 4. A single player seems not to have any cards #todo?
        return True

    def set_ownership(self, player: str, card: str, state: int) -> None:
        """
        Sets the "ownership" value for that player and card. Set a checkmark or No-card for a single box.

        :player: which player
        :card: which card
        :state: the value for the ownership state:  BLANK, HAS_CARD, DOESNT_HAVE_CARD

        example:  set_ownership("Olivia", clue.MUSTARD, HAS_CARD)
        """
        player = player.upper()
        if card not in self.game.all_cards:
            raise ValueError(card)
        if player not in self.players_names:
            raise ValueError(player)
        # self.data.get(card, {}).get(player)  # 0
        self.data[card][player] = state

    def set_fact(self, fact):
        if fact.player is None:
            self.excluded.add(fact.card)
        else:
            self.set_ownership(fact.player, fact.card, fact.card_state())

    def has_fact(self, fact) -> bool:
        """
        :return: True if the scoresheet already KNOWS the fact, False=DOESN'T know it
        """
        if fact.player is None:
            if fact.has_card:
                return self.is_excluded(fact.card)
            else:
                raise Exception(f"fact {fact} is invalid")
        return (
            self.get_ownership(fact.player, fact.card) == fact.card_state()
        )  # int == int

    def get_ownership(self, player: str, card: str) -> int:
        """
        returns a state
        Gets the "ownership" value for that player and card
        """
        player = player.upper()
        return self.data[card][player]

    # def set_card_answerstate(self, card: str, state: int) -> None:
    #     pass

    def get_ownership_cards(self, player: str, cards: List[str]) -> List[int]:
        results = []
        for card in cards:
            results.append(self.get_ownership(player, card))
        return results

    def get_owner(self, card) -> str:
        """
        :return the player who owns the card, or None if we dont know who owns it.
        """
        for player in self.players_names:
            if self.get_ownership(player, card) == clue.HAS_CARD:
                return player

        return None

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
        (Mustard)   |   |   | 0 |
        Green       |   | 0 |   |
        --Plum------|   |   |   |
        Peacock     |   |   | 1 |

        WEAPONS      | P1| P2| P3|
        ---------------------------
        --Knife------| 1 |   |   |
        Candlestick  | 0 | 0 |   |

        ROOMS        | P1| P2| P3|
        ---------------------------
        --Kitchen----| 1 |   |   |
        (Gazebo)     |   |   |   |
        """
        titles = {
            "SUSPECTS": self.game.suspects,
            "WEAPONS": self.game.weapons,
            "ROOMS": self.game.rooms,
        }
        short_names = [
            Scoresheet.short_name(s) for s in self.players_names
        ]  # HAS THE SAME ORDER AS self.players_names

        for key in titles:
            # print("")
            print(clue.INVERTED, end="")
            print(
                clue.pad_right(key, clue.longest_word(self.game.all_cards)), "|", end=""
            )
            for player in short_names:  # short names horizontally:  Dav|Oli|Xen|
                print(player, end="")
                print("|", end="")

            print(clue.NORMAL_TEXT)
            # print("----------------------------")
            for card in titles[key]:
                if self.is_excluded(card):
                    print(clue.DARK_GRAY, end="")
                elif self.is_answer(card):
                    print(clue.ANSWER_TEXT, end="")

                print(
                    clue.pad_right(card, clue.longest_word(self.game.all_cards)),
                    "|",
                    end="",
                )
                for player in self.players_names:
                    print(self.box_str(self.get_ownership(player, card)), end="")
                    print("|", end="")
                print(clue.NORMAL_TEXT, end="")
                print("")

    @staticmethod
    def short_name(player_name: str) -> str:
        """

        :param player_name:
        :return: a version of player_name that is 3 chars long, to be used as a column heading
        """
        short_name = player_name[:3]
        while len(short_name) < 3:
            short_name += " "
        return short_name

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


if __name__ == "__main__":
    sheet = Scoresheet(["A", "B", "C"], current_player="A")
    sheet.set_ownership("A", clue.GREEN, clue.HAS_CARD)
    sheet.set_ownership("A", clue.KNIFE, clue.DOESNT_HAVE_CARD)
    sheet.set_ownership("B", clue.KNIFE, clue.DOESNT_HAVE_CARD)
    sheet.set_ownership("C", clue.KNIFE, clue.DOESNT_HAVE_CARD)
    sheet.set_ownership("A", clue.FOUNTAIN, clue.HAS_CARD)
    sheet.print_scoresheet()
