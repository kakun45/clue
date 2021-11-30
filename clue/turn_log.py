from typing import Dict

import clue


class TurnLog:
    def __init__(self):
        self.entries = []


class LogEntry:
    def __init__(self, person: str, weapon: str, room: str, asker: str, answers: Dict):
        """

        :param person: the suspect that was guessed (must be a card member of the PEOPLE group)
        :param weapon: the weapon that was guessed
        :param room: the room that was guessed
        :param asker: the player who made the guess
        :param answers: the answers of the other players, in a dict where the players are the keys TODO: what are the values?
        """
        self.person = person
        self.weapon = weapon
        self.room = room
        self.asker = asker
        self.answers = answers

