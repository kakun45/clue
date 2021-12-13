import unittest

import clue
from clue import rules
from clue.scoresheet import Scoresheet
from clue.turn_log import LogEntry

class RulesTests(unittest.TestCase):

    def test_fact_equals(self):

        self.assertEqual(rules.Fact("B", clue.GREEN, False), rules.Fact("B", clue.GREEN, False))

    def test_rule1(self):

        sheet = Scoresheet(["A", "B", "C"])
        results = rules.rule_1(sheet, None)
        self.assertEqual([], results)

        sheet.set_ownership("A", clue.GREEN, clue.HAS_CARD)
        results = rules.rule_1(sheet, None)
        self.assertTrue(rules.Fact("B", clue.GREEN, False) in results)
        self.assertTrue(rules.Fact("C", clue.GREEN, False) in results)

    def test_rule1b(self):
        sheet = Scoresheet(["A", "B", "C"])
        sheet.set_ownership("A", clue.GREEN, clue.HAS_CARD)
        sheet.set_ownership("B", clue.GREEN, clue.DOESNT_HAVE_CARD)
        results = rules.rule_1(sheet, None)
        self.assertFalse(rules.Fact("B", clue.GREEN, False) in results)
        self.assertTrue(rules.Fact("C", clue.GREEN, False) in results)

    def test_rule2(self):
        turn_history = [LogEntry(clue.GREEN, clue.WRENCH, clue.STUDIO, "Dav", {"Xen": True, "Oli": False})]
        results = rules.rule_2(None, turn_history)
        self.assertEqual(3, len(results))
        self.assertTrue(rules.Fact('Oli', clue.GREEN, False))
        self.assertTrue(rules.Fact('Oli', clue.WRENCH, False))
        self.assertTrue(rules.Fact('Oli', clue.STUDIO, False))
        turn_history2 = [LogEntry(clue.GREEN, clue.WRENCH, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}),
                        LogEntry(clue.PLUM, clue.KNIFE, clue.GAZEBO, "Xen", {"Dav": False, "Oli": False})]
        results2 = rules.rule_2(None, turn_history2)
        self.assertEqual(9, len(results2))
        self.assertFalse(rules.Fact('Xen', clue.PLUM, False) in results2)

    def test_rule3(self):
        scoresheet = Scoresheet(["Dav", "Xen", "Oli"])
        turn1_history = [LogEntry(clue.PLUM, clue.KNIFE, clue.STUDIO, "Dav", {"Xen": True, "Oli": False})]
        results = rules.rule_3(scoresheet, turn1_history)
        self.assertEqual(0, len(results))
        scoresheet.set_ownership("Xen", clue.PLUM, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Xen", clue.KNIFE, clue.DOESNT_HAVE_CARD)
        turn1_history = [LogEntry(clue.PLUM, clue.KNIFE, clue.STUDIO, "Dav", {"Xen": True, "Oli": False})]
        results2 = rules.rule_3(scoresheet, turn1_history)
        self.assertEqual(1, len(results2))

        turn2_history = [LogEntry(clue.PLUM, clue.KNIFE, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}),
                         LogEntry(clue.SCARLET, clue.WRENCH, clue.STUDIO, "Xen", {"Dav": False, "Oli": False})]
        results3 = rules.rule_3(scoresheet, turn2_history)
        self.assertEqual(1, len(results3))