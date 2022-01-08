from typing import Dict


class LogEntry:
    """
    Carries info about one Guess turn
    """
    def __init__(
        self,
        suspect: str = None,
        weapon: str = None,
        room: str = None,
        asker: str = None,
        responses: Dict = None,
    ):
        """

        :param suspect: the suspect that was guessed (must be a card member of the PEOPLE group)
        :param weapon: the weapon that was guessed
        :param room: the room that was guessed
        :param asker: the player who made the guess
        :param answers: the responses of the other players, in a dict where the players are the KEYS and VALUES are True/False (true == player has card)
        """
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        self.asker = asker
        self.responses = responses or {}  # renamed answers to "responses"

    def __str__(self):
        return f"{self.asker} asks ({self.suspect}, {self.weapon}, {self.room}), answers:{self.responses}"

    def __repr__(self):
        return self.__str__()

    def is_valid(self, player_count):
        """

        :return: True if all the info is filled out and False if it's missing anything
        """
        return bool(
            self.suspect
            and self.weapon
            and self.room
            and self.asker
            and len(self.responses) == player_count - 1
        )
