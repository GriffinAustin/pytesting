import unittest

from pytesting import testing

tester = testing.Test(testing.WarningLevels.HIGH)


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
        self.assertTrue(tester.assert_false(False))


class TestDecorators(testing.Test):
    @testing.skip("test skip decorator")
    def test_skip(self):
        raise AssertionError

    @testing.skip_if(True, "test skip_if decorator when True")
    def test_skip_if_true(self):
        raise AssertionError

    @testing.skip_if(False, "test skip_if decorator when False")
    def test_skip_if_false(self):
        self.assert_true(True)

    @testing.skip_unless(False, "test skip_unless decorator when False")
    def test_skip_unless_false(self):
        raise AssertionError

    @testing.skip_unless(True, "test skip_unless decorator when True")
    def test_skip_unless_true(self):
        self.assert_true(True)


testsuite = TestDecorators(testing.WarningLevels.HIGH)
testsuite.run_tests()
