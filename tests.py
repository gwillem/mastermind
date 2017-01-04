from unittest import TestCase
from game import Combo, Game, tuple_intersection, tuple_match


class TestMasterMind(TestCase):

    def _assert_compare(self, a, b, red, white):

        got = Game.verdict(Combo(a), Combo(b))
        want = (red, white)

        self.assertEqual(got, want, 
            "{} vs {} produced r:{} and w:{}".format(a, b, red, white)
        )

    def test_compare_no_matches(self):
        self._assert_compare((1, 2, 2, 4), (5, 5, 5, 5), 0, 0)

    def test_compare_all_red(self):
        self._assert_compare((1, 2, 2, 4), (1, 2, 2, 4), 4, 0)

    def test_compare_all_white(self):
        self._assert_compare((1, 2, 3, 4), (4, 3, 2, 1), 0, 4)

    def test_compare_two_white_two_red(self):
        self._assert_compare((1, 2, 3, 4), (1, 4, 3, 2), 2, 2)

    def test_compare_more_colors_one_red(self):
        self._assert_compare((1, 1, 1, 1), (1, 0, 0, 0), 1, 0)
        # and in reverse
        self._assert_compare((1, 0, 0, 0), (1, 1, 1, 1), 1, 0)

    def test_compare_two_white(self):
        self._assert_compare((1, 1, 0, 0), (8, 1, 1, 1), 1, 1)

    def test_compare_zero_index(self):
        self._assert_compare((0, 8, 2, 2), (6, 7, 3, 0), 0, 1)


class TestMasterMindHelpers(TestCase):

    def test_tuple_intersection(self):

        i = tuple_intersection((1,2,3,4), (3,4,5,6))
        self.assertEqual(i, 2)

    def test_tuple_match_fails_wrong_size(self):

        with self.assertRaises(AssertionError):
            i = tuple_match((1,2,3,4), (3,4,5,6, 7))

    def test_tuple_match_no_match(self):

        i = tuple_match((1,2,3,4), (3,4,5,6))
        self.assertEqual(i, 0)

    def test_tuple_match(self):
        i = tuple_match((1,2,3,4), (1,4,5,6))
        self.assertEqual(i, 1)
