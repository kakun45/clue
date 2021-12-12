import unittest

import clue
from clue.repl import ClueRepl
from clue.scoresheet import Scoresheet
from clue.turn_log import LogEntry


class ReplTests(unittest.TestCase):

    @staticmethod
    def _ss():
        return Scoresheet(["P1", "P2", "P3"])

    def test_resolve_card(self):
        repl = ClueRepl(self._ss())
        self.assertEqual([clue.MUSTARD], repl.resolve_card("Mu"))
        self.assertEqual([clue.MUSTARD], repl.resolve_card("MU"))
        self.assertEqual([clue.MUSTARD], repl.resolve_card("mu"))
        self.assertEqual(sorted([clue.DINING, clue.DRAWING]), sorted(repl.resolve_card("d")))
        self.assertEqual([], repl.resolve_card("z"))
        self.assertEqual([clue.PLUM], repl.resolve_card("plum"))

    def test_parse_line(self):
        repl = ClueRepl(self._ss())

        asker, cards, answers = repl.parse_line("P1 plum P2=yes")
        self.assertEqual(asker, "P1")
        self.assertEqual(cards, [clue.PLUM])
        self.assertEqual(answers, [("P2", True)])

        asker, cards, answers = repl.parse_line("p1 plum P2=yes")
        self.assertEqual(asker, "P1")
        self.assertEqual(cards, [clue.PLUM])
        self.assertEqual(answers, [("P2", True)])

    def test_response_bool(self):
        self.assertEqual(True, ClueRepl.response_bool("yes"))
        self.assertEqual(False, ClueRepl.response_bool("NOne"))
        self.assertEqual(False, ClueRepl.response_bool("NOpe"))
        with self.assertRaises(Exception):
            ClueRepl.response_bool("Nrtrt")

    def test_update_entry(self):
        log_entry = LogEntry()

        ClueRepl.update_entry(log_entry, asker="Dave", cards=[], answers=[])
        self.assertEqual("Dave", log_entry.asker)
        ClueRepl.update_entry(log_entry, asker="Dave", cards=[clue.KNIFE], answers=[])
        self.assertEqual(clue.KNIFE, log_entry.weapon)
        ClueRepl.update_entry(log_entry, asker="Dave", cards=[clue.KNIFE, clue.DRAWING], answers=[('olivia', True)])
        self.assertEqual(clue.DRAWING, log_entry.room)
        self.assertEqual(log_entry.responses["olivia"], True)

    def test_parse_set_line(self):
        line = "set plum dave=yes"
        self.assertEqual(([clue.PLUM], "dave", clue.HAS_CARD), ClueRepl.parse_set_line(line))
        line2 = "set KNI dave=N"
        self.assertEqual(([clue.KNIFE], "dave", clue.DOESNT_HAVE_CARD), ClueRepl.parse_set_line(line2))
        line3 = "set plu kni dini dave=y"
        ClueRepl.parse_set_line(line3)