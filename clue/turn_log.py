from typing import Dict

import clue


# class TurnLog:
#     def __init__(self):
#         self.entries = []
#
#     def append(self, entry):
#         self.entries.append(entry)


class LogEntry:
    def __init__(self, suspect: str = None, weapon: str = None, room: str = None, asker: str = None, answers: Dict = None):
        """

        :param suspect: the suspect that was guessed (must be a card member of the PEOPLE group)
        :param weapon: the weapon that was guessed
        :param room: the room that was guessed
        :param asker: the player who made the guess
        :param answers: the responses of the other players, in a dict where the players are the keys TODO: what are the values?
        """
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        self.asker = asker
        self.answers = answers or {}  # TODO rename to "responses"

    def __str__(self):
        # return f"suspect:{self.suspect}, weapon:{self.weapon}, room:{self.room}, asker:{self.asker}, answers:{self.answers}"
        return f"{self.asker} asks ({self.suspect}, {self.weapon}, {self.room}), answers:{self.answers}"

