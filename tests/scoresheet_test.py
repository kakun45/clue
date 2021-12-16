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
        scoresheet.set_ownership("DAVE", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_answer(clue.PLUM))
        scoresheet.set_ownership("OLIVIA", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_answer(clue.PLUM))
        scoresheet.set_ownership("XENIYA", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertTrue(scoresheet.is_answer(clue.PLUM))

    def test_box_str(self):
        result = Scoresheet.box_str(clue.DOESNT_HAVE_CARD)
        self.assertEqual(" 0 ", result)

    def test_is_valid(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("OLIVIA", clue.FOUNTAIN, clue.HAS_CARD)
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("XENIYA", clue.FOUNTAIN, clue.HAS_CARD)
        self.assertFalse(scoresheet.is_valid())

    def test_is_valid2(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Olivia", clue.PLUM, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.BRUNETTE, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Olivia", clue.BRUNETTE, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.BRUNETTE, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_valid())

    def test_is_valid3(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.BRUNETTE, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Olivia", clue.BRUNETTE, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.BRUNETTE, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Xeniya", clue.WRENCH, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Olivia", clue.WRENCH, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.WRENCH, clue.DOESNT_HAVE_CARD)
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.REVOLVER, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Olivia", clue.REVOLVER, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.REVOLVER, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_valid())

    def test_is_valid3(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.STUDIO, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Olivia", clue.STUDIO, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.STUDIO, clue.DOESNT_HAVE_CARD)
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.LIBRARY, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Olivia", clue.LIBRARY, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.LIBRARY, clue.DOESNT_HAVE_CARD)
        self.assertFalse(scoresheet.is_valid())

    def test_is_valid4(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.KNIFE, clue.HAS_CARD)
        self.assertTrue(scoresheet.is_valid())
        scoresheet.set_ownership("Xeniya", clue.CANDLESTICK, clue.HAS_CARD)
        scoresheet.set_ownership("Xeniya", clue.REVOLVER, clue.HAS_CARD)
        scoresheet.set_ownership("Xeniya", clue.ROPE, clue.HAS_CARD)
        scoresheet.set_ownership("Xeniya", clue.PIPE, clue.HAS_CARD)
        scoresheet.set_ownership("Xeniya", clue.WRENCH, clue.HAS_CARD)
        scoresheet.set_ownership("Xeniya", clue.POISON, clue.HAS_CARD)
        scoresheet.set_ownership("Xeniya", clue.HORSESHOE, clue.HAS_CARD)
        self.assertFalse(scoresheet.is_valid())

    def test_get_owner(self):
        scoresheet = Scoresheet(["Dave", "Olivia", "Xeniya"])
        self.assertIsNone(scoresheet.get_owner(clue.PLUM))
        scoresheet.set_ownership("Dave", clue.PLUM, clue.DOESNT_HAVE_CARD)
        self.assertIsNone(scoresheet.get_owner(clue.PLUM))
        scoresheet.set_ownership("Dave", clue.PLUM, clue.HAS_CARD)
        self.assertEqual("DAVE", scoresheet.get_owner(clue.PLUM).upper())

    def test_get_ownership_cards(self):
        scoresheet = Scoresheet(["Dave", "Xeniya", "Olivia"])
        self.assertEqual([clue.BLANK, clue.BLANK, clue.BLANK],
                         scoresheet.get_ownership_cards("Dave", [clue.PLUM, clue.KNIFE, clue.STUDIO]))
        scoresheet.set_ownership("Dave", clue.KNIFE, clue.DOESNT_HAVE_CARD)
        scoresheet.set_ownership("Dave", clue.STUDIO, clue.DOESNT_HAVE_CARD)
        self.assertEqual([clue.BLANK, clue.DOESNT_HAVE_CARD, clue.DOESNT_HAVE_CARD],
                         scoresheet.get_ownership_cards("Dave", [clue.PLUM, clue.KNIFE, clue.STUDIO]))