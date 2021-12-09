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

            try:
                if line.strip().lower() == "quit":
                    return
                elif line.strip().lower() == "sheet":
                    self.scoresheet.print_scoresheet()
                elif line.strip().lower().startswith("set "):  # can change to 'owner'
                    cards, player, state = ClueRepl.parse_set_line(line)
                    for card in cards:
                        self.scoresheet.set_ownership(player, card, state)

                else:
                    asker, cards, answers = self.parse_line(line)
                    ClueRepl.update_entry(current_entry, asker, cards, answers)

            except Exception as ex:
                print(ex)

    @staticmethod
    def parse_set_line(line):
        """
        :param line: is a line like "set plum dave=yes"   |  yes,no, or ? for blank ... or even 'set plum dave=' for blank
        :return
        """
        line = line.strip().lower()
        tokens = line.split()
        cards = []
        if len(tokens) < 3 or "=" not in tokens[-1]:
            raise Exception(f"Invalid 'set <card> player=' line: {line}")
        if tokens[0] != "set":
            raise Exception()

        for card in tokens[1:-1]:  # it must be clue cards
            matches = ClueRepl.resolve_card(card)  # this will return ["Dining", "drawing"] if input "d"
            if len(matches) != 1:
                # we don't know which card they meant
                raise Exception(f"bad input: unable to match '{card}' to a single card.  Matches={matches}")
            cards.append(matches[0])
        player, response = tokens[-1].split("=", maxsplit=1)
        if response == '':
            state = clue.BLANK
        elif ClueRepl.response_bool(response):
            state = clue.HAS_CARD
        else:
            state = clue.DOESNT_HAVE_CARD
        return cards, player, state  # ([clue.PLUM]: List, "dave": str, clue.HAS_CARD: int)

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
            player, response = a  # a - tuple of two things
            current_entry.answers[player] = response

    @staticmethod  # validate answers:'y','n','nope','none','nothing','i_have_one' ...
    def response_bool(s: str) -> bool:
        truthy = ["y", "yes", 'yep', "have", "has", "true", "do"]
        falsy = ["n", "no", 'not', "nope", "none", "false", "don't", "nothing"]
        if s.lower() in truthy:
            return True
        elif s.lower() in falsy:
            return False
        else:
            raise Exception(f"invalid entry: {s}")

    def parse_line(self, line):  # TODO rename to something like parse_guess_line
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
