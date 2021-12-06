import copy
from typing import List, Tuple

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

    def do_input(self):
        current_entry = turn_log.LogEntry()
        while True:
            print(f"current entry: {current_entry}")
            line = input("> ")
            if line.strip().lower() == "quit":
                return

            try:
                asker, cards, answers = self.parse_line(line)
                ClueRepl.update_entry(current_entry, asker, cards, answers)

            except Exception as ex:
                print(ex)

    @staticmethod
    def update_entry(current_entry, asker: str, cards: List[str], answers: List[Tuple[str, bool]]):
        """
        Updates `current_entry` using information parsed from parse_line()
        :param current_entry:  the entry object to modify
        :param asker:  the "asker" returned by parse_line(); should be None if there was no asker in the line
        :param cards:  list of cards returned by parse_line()
        :param answers:   list of tuples of (player:str, response:bool))
        """
        if asker:
            current_entry.asker = asker
        suspect = None
        weapon = None
        room = None
        for card in cards:
            if card in clue.PEOPLE:
                if suspect:
                    raise Exception(f"Two suspects in one line are not accepted: {suspect}, {card}")
                else:
                    suspect = card
            elif card in clue.ROOMS:
                if room:
                    raise Exception(f"Two rooms in one line are not accepted: {room}, {card}")
                else:
                    room = card
            elif card in clue.WEAPONS:
                if weapon:
                    raise Exception(f"Two weapons in one line are not accepted: {weapon}, {card}")
                else:
                    weapon = card

        if suspect:
            current_entry.suspect = suspect
        if weapon:
            current_entry.weapon = weapon
        if room:
            current_entry.room = room

        for a in answers:  # answers - list of tuples
            player, response = a
            current_entry.answers[player] = response

    @staticmethod  # validate answers:'y','n','nope','none','nothing','i_have_one' ...
    def response_bool(s: str) -> bool:
        truthy = ["y", "yes", 'yep', "have", "has", "true", "do"]
        falsy = ["n", "no", "nope", "none", "false", "don't", "nothing"]
        if s.lower() in truthy:
            return True
        elif s.lower() in falsy:
            return False
        else:
            raise Exception(f"invalid entry: {s}")

    def parse_line(self, line):
        tokens = line.strip().split()
        asker = None
        cards = []
        answers = []

        for token in tokens:  # when you parse a str you parse it into pieces - tokens
            if token.upper() in self.scoresheet.players_names:  # it must be the asker
                asker = token.upper()
            elif "=" in token:
                player, response = token.split("=", maxsplit=1)  # maxsplit is number of times to use split()
                # make sure its a valid player! split on '=' also if bob=yes => error
                if player.upper() not in self.scoresheet.players_names:
                    raise Exception(f"bad input: invalid player {player}")
                answers.append((player, ClueRepl.response_bool(response)))
            else:
                # it must be a clue card
                matches = ClueRepl.resolve_card(token)  # this will return ["Dining", "drawing"] if input "d"
                if len(matches) != 1:
                    # we don't know which card they meant
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
