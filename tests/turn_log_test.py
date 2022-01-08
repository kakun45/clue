import unittest

import clue
from clue.turn_log import LogEntry


class TurnLogTests(unittest.TestCase):
    def test_is_valid(self):
        data = LogEntry()
        # self.assertEqual(False, data.is_valid(4))
        self.assertFalse(data.is_valid(4))

        data2 = LogEntry(
            suspect=clue.SCARLET,
            weapon=clue.KNIFE,
            room=clue.STUDIO,
            asker="Dave",
            responses={"A": True, "B": False, "C": True},
        )
        # self.assertEqual(True, data2.is_valid(4))
        self.assertTrue(data2.is_valid(4))

        data3 = LogEntry(
            suspect=clue.SCARLET,
            weapon=clue.KNIFE,
            room=clue.STUDIO,
            asker="Dave",
            responses={"A": True, "C": True},
        )
        self.assertFalse(data3.is_valid(4))

        data2 = LogEntry(
            suspect=clue.SCARLET,
            room=clue.STUDIO,
            asker="Dave",
            responses={"A": True, "B": False, "C": True},
        )
        self.assertFalse(data2.is_valid(4))

        data2 = LogEntry(
            weapon=clue.KNIFE,
            room=clue.STUDIO,
            asker="Dave",
            responses={"A": True, "B": False, "C": True},
        )
        self.assertFalse(data2.is_valid(4))

        data2 = LogEntry(
            suspect=clue.SCARLET,
            weapon=clue.KNIFE,
            asker="Dave",
            responses={"A": True, "B": False, "C": True},
        )
        self.assertFalse(data2.is_valid(4))
