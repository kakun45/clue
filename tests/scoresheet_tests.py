import unittest

import clue
from clue.scoresheet import Scoresheet


class ScoresheetTests(unittest.TestCase):

    def test_set_ownership(self):
        # expected on the left, Actual on the right
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertEqual(scoresheet.get_ownership("Olivia", clue.PLUM), clue.BLANK)
        scoresheet.set_ownership("Olivia", clue.PLUM, clue.HAS_CARD)
        self.assertEqual(scoresheet.get_ownership("Olivia", clue.PLUM), clue.HAS_CARD)
        self.assertEqual(scoresheet.get_ownership("Xeniya", clue.PLUM), clue.BLANK)

    def test_knife(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertEqual(scoresheet.get_ownership("Dave", clue.KNIFE), clue.BLANK)

    def test_set_is_excluded(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertFalse(scoresheet.is_excluded(clue.KITCHEN))
        scoresheet.set_excluded(clue.KITCHEN)
        self.assertTrue(scoresheet.is_excluded(clue.KITCHEN))

        self.assertFalse(scoresheet.is_excluded(clue.FOUNTAIN))
        scoresheet.set_ownership("Xeniya", clue.FOUNTAIN, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_excluded(clue.FOUNTAIN))
        scoresheet.set_ownership("Olivia", clue.FOUNTAIN, clue.HAS_CARD)
        self.assertTrue(scoresheet.is_excluded(clue.FOUNTAIN))

    def test_is_answer(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertFalse(scoresheet.is_answer(clue.PLUM))
        scoresheet.set_ownership("Dave", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_answer(clue.PLUM))
        scoresheet.set_ownership("Olivia", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_answer(clue.PLUM))
        scoresheet.set_ownership("Xeniya", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertTrue(scoresheet.is_answer(clue.PLUM))

    def test_box_str(self):
        result = Scoresheet.box_str(clue.DOESNT_HAVE_CARD)
        self.assertEqual(" 0 ", result)
