from typing import List, Tuple

import clue
import clue.rules
from clue import turn_log


class ClueRepl:
    """
    This will grab input from the user and then update the log and scoresheet.

    > dave knif plum di olivia=no
    input:  "dave knif plum di olivia=no"
    tokens:  {player: "dave"}, {card: knife}, {card: plum}, {card: dining}, {card:..}

    """

    def __init__(self, scoresheet):
        self.scoresheet = scoresheet  # this is NOT the module scoresheet.py
        for player in scoresheet.players_names:
            assert player not in scoresheet.game.all_cards
            assert "=" not in player

        # self.current_entry = turn_log.LogEntry()

    @staticmethod
    def prompt_players_list() -> List[str]:
        """
        data = Scoresheet(["Dave", "Olivia", "Xeniya"])
        """
        players_list = []
        line = input("Enter the # of players > ")
        print(
            "Enter the player names in the order they should appear on the scoresheet"
        )
        number_of_players = int(line)
        for player in range(number_of_players):
            name = input(f"Name Player {player + 1} > ").strip()
            players_list.append(name)
        return players_list

    @staticmethod
    def select_player(player_list: List[str]) -> str:
        """
        Prints a list like:
        0) Player A
        1) Player B
        2) Player C
            select which player you are> 1

        :param player_list:
        :return: str
        """
        for i, player in enumerate(player_list):
            print(f"{i+1}) Player {player}")
        while True:
            try:
                line = int(input("select which player you are> "))
                return player_list[line - 1]
            except ValueError:
                print(f"It MUST be a number.")

    def analyze(self, turn_history):
        print("Analysis Results:")
        # need to do more passes until run_all() returns empty list
        while True:
            results = clue.rules.run_all(self.scoresheet, turn_history)
            for result in results:
                print(result)
                self.scoresheet.set_fact(result)
            if len(results) < 1:
                break
            else:
                print("....")
        print("")

    def do_input(self):
        current_entry = turn_log.LogEntry()
        turn_history = []
        while True:
            print(f"Current Turn({len(turn_history) + 1}): {current_entry}")
            line = input("> ")

            try:
                if line.strip().lower() == "quit":
                    return
                elif line.strip().lower() == "sheet":
                    self.scoresheet.print_scoresheet()
                elif line.strip().lower().startswith("set "):  # can change to 'owner'
                    cards, player, state = ClueRepl.parse_set_line(
                        self.scoresheet.game, line
                    )
                    for card in cards:
                        self.scoresheet.set_ownership(player, card, state)
                        # print(f"scoresheet.data[card][player] = state")
                        if state == clue.BLANK:
                            print(f"setting {player} and {card} to 'unknown' ")
                        else:
                            verb = {
                                clue.HAS_CARD: "has",
                                clue.DOESNT_HAVE_CARD: "doesn't have",
                            }.get(state)
                            print(f"marking: {player} {verb} {card}")

                elif line.strip().lower() == "next":
                    # check if anything is missing before allowing the player to go to the next turn
                    if current_entry.is_valid(self.scoresheet.player_count()):
                        turn_history.append(current_entry)
                        current_entry = turn_log.LogEntry()
                        self.analyze(turn_history)  # runs "next" & "analyze"
                    else:
                        print(f"Current turn is not finished: {current_entry}")

                elif line.strip().lower() == "clear":  # clears out wrong current_entry
                    # command that resets the current entry:
                    current_entry = turn_log.LogEntry()
                elif line.strip().lower() == "history":  # prints out the turn history
                    for i, x in enumerate(turn_history):
                        print(i + 1, x)

                elif line.strip().lower() == "analyze":
                    self.analyze(turn_history)

                else:
                    asker, cards, answers = self.parse_line(line)
                    should_update = True
                    # don't let them put the same player as both "asker" and in the responses on the same line ONLY.
                    # and have a 'reset' command that resets the current entry from:
                    # Current Turn(2): B asks (Plum, Wrench, Gazebo), answers:{'a': False, 'b': True}

                    # print(f"asker={asker} answers={answers}")
                    asker_has_responded = [i for i in answers if asker in i]
                    if asker_has_responded:
                        print(f"Warning: Did you put the asker in responses?")
                        should_update = False
                    # confirm when I'm about overwrite existing info of a turn b4 removing a previous player
                    if asker and current_entry.asker and asker != current_entry.asker:
                        print(f"Warning: Did you forget to type 'next'?")
                        yn = input(
                            f"Enter 'y' to change the asker from {current_entry.asker} to {asker}. y/n>"
                        )

                        should_update = bool(yn.strip().lower() == "y")
                        # if yn.strip().lower() == "y":
                        #     should_update = True
                        # else:
                        #     should_update = False

                    if should_update:
                        ClueRepl.update_entry(
                            self.scoresheet.game, current_entry, asker, cards, answers
                        )
                        if current_entry.asker in current_entry.responses:
                            print(
                                f"WARNING:  {current_entry.asker} is both the 'asker' and one of the responses"
                            )
                    else:
                        print(f"ignoring this input: {line}")

            except Exception as ex:  # pylint: disable=broad-except
                print(ex)

    @staticmethod
    def parse_set_line(game, line):
        """
        :param game:
        :param line: is a line like "set plum dave=yes"   |  yes,no, or ? for blank ... or even 'set plum dave=' for blank
        :return: ([clue.PLUM]: List, "dave": str, clue.HAS_CARD: int)
        """
        line = line.strip().lower()
        tokens = line.split()
        cards = []
        if len(tokens) < 3 or "=" not in tokens[-1]:
            raise Exception(f"Invalid 'set <card> player=' line: {line}")
        if tokens[0] != "set":
            raise Exception()

        for card in tokens[1:-1]:  # it must be clue cards
            # this will return ["Dining", "Drawing"] if input "d":
            matches = ClueRepl.resolve_card(game, card)
            if len(matches) != 1:
                # we don't know which card they meant
                raise Exception(
                    f"bad input: unable to match '{card}' to a single card.  Matches={matches}"
                )
            cards.append(matches[0])
        player, response = tokens[-1].split("=", maxsplit=1)
        if response == "":
            state = clue.BLANK
        elif ClueRepl.response_bool(response):
            state = clue.HAS_CARD
        else:
            state = clue.DOESNT_HAVE_CARD
        return (
            cards,
            player,
            state,
        )  # -> ([clue.PLUM]: List, "dave": str, clue.HAS_CARD: int)

    @staticmethod
    def update_entry(
        game: clue.Game,
        current_entry,
        asker: str,
        cards: List[str],
        answers: List[Tuple[str, bool]],
    ):
        """
        Updates `current_entry` using information parsed from parse_line()
        :param game:
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
            if card in game.suspects:
                if suspect:
                    raise Exception(
                        f"Two suspects in one line are not accepted: {suspect}, {card}"
                    )
                else:
                    suspect = card
            elif card in game.rooms:
                if room:
                    raise Exception(
                        f"Two rooms in one line are not accepted: {room}, {card}"
                    )
                else:
                    room = card
            elif card in game.weapons:
                if weapon:
                    raise Exception(
                        f"Two weapons in one line are not accepted: {weapon}, {card}"
                    )
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
            current_entry.responses[player] = response

    @staticmethod  # validate answers:'y','n','nope','none','nothing','i_have_one' ...
    def response_bool(s: str) -> bool:
        truthy = ["y", "yes", "yep", "have", "has", "t", "true", "do"]
        falsy = [
            "n",
            "no",
            "not",
            "nope",
            "none",
            "f",
            "false",
            "don't",
            "dont",
            "nothing",
        ]
        if s.lower() in truthy:
            return True
        elif s.lower() in falsy:
            return False
        else:
            raise Exception(f"invalid entry: {s}")

    def parse_line(self, line):
        """
        This parses an input str from a user on a 'guess' turn into tokens. Maybe rename to smt like parse_guess_line
        :param line: asker card card card responder1=yes responder2=no
        :return: tokens
        """
        tokens = line.strip().split()
        asker = None
        cards = []
        answers = []

        for token in tokens:  # when you parse a str you parse it into pieces - tokens
            if token.upper() in self.scoresheet.players_names:  # it must be the asker
                asker = token.upper()
            elif "=" in token:
                player, response = token.split(
                    "=", maxsplit=1
                )  # maxsplit is number of times to use split()
                # make sure its a valid player! split on '=' also if bob=yes => error
                if player.upper() not in self.scoresheet.players_names:
                    raise Exception(f"bad input: invalid player {player}")
                answers.append((player.upper(), ClueRepl.response_bool(response)))
            else:
                # it must be a clue card
                matches = ClueRepl.resolve_card(
                    self.scoresheet.game, token
                )  # this will return ["Dining", "Drawing"] if input "d"
                if len(matches) != 1:
                    # we don't know which card they meant
                    raise Exception(
                        f"bad input: unable to match {token} to a single card.  Matches={matches}"
                    )
                cards.append(matches[0])
        return asker, cards, answers

    @staticmethod
    def resolve_card(game: clue.Game, prefix: str) -> List[str]:
        """
            # prefix="gr"  ->   ["GREEN"]
            # prefix="D"   ->   ["DINING", "DRAWING"]
            # prefix="z"   ->   []
        :return: list of EVERY card that matches prefix
        """
        results = []
        prefix = prefix.upper()
        for card in game.all_cards:
            if card.upper().startswith(prefix):
                results.append(card)
        return results
