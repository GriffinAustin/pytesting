import unittest

from pytesting import testing

tester = testing.Test()


class TestAssertionMethods(unittest.TestCase):
    def test_assert_equal(self):
        self.assertEqual(
            tester.assert_equal(None, None),
            True
        )
        self.assertEqual(
            tester.assert_equal(0, 0),
            True
        )
        self.assertEqual(
            tester.assert_equal("string", "string"),
            True
        )

    def test_assert_unequal(self):
        self.assertEqual(
            tester.assert_unequal(None, 0),
            True
        )
        self.assertEqual(
            tester.assert_unequal(1, -1),
            True
        )
        self.assertEqual(
            tester.assert_unequal("string", 0),
            True
        )

    def test_assert_true(self):
        self.assertTrue(tester.assert_true(True))

    def test_assert_false(self):
        self.assertFalse(not tester.assert_false(False))
