import unittest

import clue
from clue.repl import ClueRepl
from clue.scoresheet import Scoresheet


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
        self.assertEqual(answers, ["P2=yes"])

        asker, cards, answers = repl.parse_line("p1 plum P2=yes")
        self.assertEqual(asker, "P1")
        self.assertEqual(cards, [clue.PLUM])
        self.assertEqual(answers, ["P2=yes"])
