from typing import List

import clue
from clue import turn_log


class ClueRepl:
    """
    This will grab input from the user and then update the log and scoresheet.

    > dave knif plum di olivia=no
    input:  "dave knif plum di olivia=no"
    tokens:  {player: "dave"}, {card: knife}, {card: plum}, {card: dining}, {card




    """
    def __init__(self, scoresheet):
        self.scoresheet = scoresheet
        for player in scoresheet.players_names:
            assert player not in clue.ALL_CARDS
            assert "=" not in player

        # self.current_entry = turn_log.LogEntry()

    def parse_line(self, line):
        tokens = line.strip().split()
        asker = None
        cards = []
        answers = []

        # TODO: make the player name testing case insensitive

        for token in tokens:
            if token in self.scoresheet.players_names:
                # it must be the asker
                asker = token
            elif "=" in token:
                # player answer
                # TODO make sure its a valid player! maybe split on = also
                answers.append(token)
            else:
                # it must be a clue card
                matches = ClueRepl.resolve_card(token)  # this will return ["Dining", "drawing"] if input "d"
                if len(matches) != 1:
                    # we dont know which card they meant
                    raise Exception(f"bad input: unable to match {token} to a single card.  Matches={matches}")
                cards.append(matches[0])
        return asker, cards, answers



    @staticmethod
    def resolve_card(prefix: str) -> List[str]:
        """
            # prefix="gr"  ->   ["GREEN"]
            # prefic="D"   ->   ["DINING", "DRAWING"]
            # prefix="z"   ->   []
        :return: list of EVERY card that matches prefix
        """
        results = []
        prefix = prefix.upper()
        for card in clue.ALL_CARDS:
            if card.upper().startswith(prefix):
                results.append(card)
        return results
