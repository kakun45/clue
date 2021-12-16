import unittest

import clue

class InitTests(unittest.TestCase):

    def test_test_longest(self):
        self.assertEqual(clue.longest_word(clue.MASTER_DETECTIVE.all_cards), 14)

    def test_pad_right(self):
        self.assertEqual("abc", clue.pad_right("abc", 0))
        self.assertEqual("abc", clue.pad_right("abc", 3))
        self.assertEqual("abc ", clue.pad_right("abc", 4))
        self.assertEqual("abc  ", clue.pad_right("abc", 5))
        self.assertEqual("abcabcabc ", clue.pad_right("abcabcabc", 10))

    def test_green_game(self):
        self.assertEqual(6, len(clue.GREEN_BOARD.suspects))
        self.assertEqual(6, len(clue.GREEN_BOARD.weapons))
        self.assertEqual(9, len(clue.GREEN_BOARD.rooms))
