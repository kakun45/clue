import unittest

import clue
from clue import rules
from clue.scoresheet import Scoresheet
from clue.turn_log import LogEntry


class RulesTests(unittest.TestCase):
    def test_fact_equals(self):

        self.assertEqual(
            rules.Fact("B", clue.GREEN, False), rules.Fact("B", clue.GREEN, False)
        )

    def test_rule1(self):

        sheet = Scoresheet(["A", "B", "C"], current_player="A")
        results = rules.rule_1(sheet, None)
        self.assertEqual([], results)

        sheet.set_ownership("A", clue.GREEN, clue.HAS_CARD)
        results = rules.rule_1(sheet, None)
        self.assertTrue(rules.Fact("B", clue.GREEN, False) in results)
        self.assertTrue(rules.Fact("C", clue.GREEN, False) in results)

    def test_rule1b(self):
        sheet = Scoresheet(["A", "B", "C"], current_player="A")
        sheet.set_ownership("A", clue.GREEN, clue.HAS_CARD)
        sheet.set_ownership("B", clue.GREEN, clue.DOESNT_HAVE_CARD)
        results = rules.rule_1(sheet, None)
        self.assertFalse(rules.Fact("B", clue.GREEN, False) in results)
        self.assertTrue(rules.Fact("C", clue.GREEN, False) in results)

    def test_rule2(self):
        turn_history = [
            LogEntry(
                clue.GREEN, clue.WRENCH, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}
            )
        ]
        results = rules.rule_2(None, turn_history)
        self.assertEqual(3, len(results))
        self.assertTrue(rules.Fact("Oli", clue.GREEN, False))
        self.assertTrue(rules.Fact("Oli", clue.WRENCH, False))
        self.assertTrue(rules.Fact("Oli", clue.STUDIO, False))
        turn_history2 = [
            LogEntry(
                clue.GREEN, clue.WRENCH, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}
            ),
            LogEntry(
                clue.PLUM, clue.KNIFE, clue.GAZEBO, "Xen", {"Dav": False, "Oli": False}
            ),
        ]
        results2 = rules.rule_2(None, turn_history2)
        self.assertEqual(9, len(results2))
        self.assertFalse(rules.Fact("Xen", clue.PLUM, False) in results2)

    def test_rule3(self):
        scoresheet = Scoresheet(["Dav", "Xen", "Oli"], current_player="Dav")
        turn1_history = [
            LogEntry(
                clue.PLUM, clue.KNIFE, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}
            )
        ]
        results = rules.rule_3(scoresheet, turn1_history)
        self.assertEqual(0, len(results))
        scoresheet.set_ownership("Xen", clue.PLUM, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Xen", clue.KNIFE, clue.DOESNT_HAVE_CARD)
        turn1_history = [
            LogEntry(
                clue.PLUM, clue.KNIFE, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}
            )
        ]
        results2 = rules.rule_3(scoresheet, turn1_history)
        self.assertEqual(1, len(results2))

        turn2_history = [
            LogEntry(
                clue.PLUM, clue.KNIFE, clue.STUDIO, "Dav", {"Xen": True, "Oli": False}
            ),
            LogEntry(
                clue.SCARLET,
                clue.WRENCH,
                clue.STUDIO,
                "Xen",
                {"Dav": False, "Oli": False},
            ),
        ]
        results3 = rules.rule_3(scoresheet, turn2_history)
        self.assertEqual(1, len(results3))

    def test_rule4(self):
        scoresheet = Scoresheet(["Dav", "Xen", "Oli"], current_player="Dav")
        results = rules.rule_4(scoresheet, [])
        self.assertEqual(0, len(results))

        scoresheet.set_ownership("Dav", clue.KNIFE, clue.HAS_CARD)
        results = rules.rule_4(scoresheet, [])
        self.assertEqual(0, len(results))
        scoresheet.set_ownership("Dav", clue.HORSESHOE, clue.DOESNT_HAVE_CARD)

        for card in [c for c in clue.MASTER_DETECTIVE.weapons if c != clue.HORSESHOE]:
            scoresheet.set_ownership("Dav", card, clue.HAS_CARD)

        results = rules.rule_4(scoresheet, [])
        self.assertEqual(3, len(results))

    def test_rule5(self):
        scoresheet = Scoresheet(["A", "B", "C", "D"], current_player="D")
        scoresheet.set_ownership("B", clue.PLUM, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("C", clue.PLUM, clue.DOESNT_HAVE_CARD)
        for card in [clue.PLUM, clue.KNIFE, clue.STUDIO]:
            scoresheet.set_ownership("D", card, clue.DOESNT_HAVE_CARD)
        turn_history = [
            LogEntry(
                clue.PLUM,
                clue.KNIFE,
                clue.STUDIO,
                "A",
                {"B": True, "C": True, "D": False},
            )
        ]
        results = rules.rule_5(scoresheet, turn_history)
        self.assertEqual(2, len(results))
        for r in results:
            self.assertTrue(r.player is None)
            self.assertTrue(r.has_card)
            self.assertTrue(r.card in [clue.STUDIO, clue.KNIFE])
