import inspect
import os
import sys
import time
import traceback
from enum import Enum


class TestBase:
    def __init__(self, warning_level):
        self.proc_time = 0
        self.warning_level = warning_level
        self.num_successful = 0
        self.num_failed = 0
        self.num_errored = 0
        self.num_skipped = 0

    def _assembly(self):
        """Call once before any other test methods."""
        pass

    def _disassembly(self):
        """Call once after all other test methods."""
        num_tests = self.num_successful + self.num_failed + self.num_errored
        print("Ran {:d} tests in {:.3f} seconds\n{:d} succeeded, {:d} failed, {:d} errored, {:d} skipped"
              .format(num_tests, self.proc_time, self.num_successful, self.num_failed, self.num_errored,
                      self.num_skipped))

    def assert_equal(self, first, second):
        """Compare two values, raising exception on failure and error."""
        try:
            if first == second:
                self.num_successful += 1
                return True
            elif type(first) == type(second):  # If first and second are not equal but are of same type
                raise Handler.NotEqualFailure(first, second)
            else:  # If first and second are not of same type
                raise Handler.NotComparableError(first, second)
        except Handler.NotComparableError as e:
            self.num_errored += 1
            handle_unsuccess(e, self.warning_level)
        except Handler.NotEqualFailure as f:
            self.num_failed += 1
            handle_unsuccess(f, self.warning_level)
            return False


class Test(TestBase):
    def __init__(self, warning_level=None):
        if warning_level is None:
            self.warning_level = WarningLevels.HIGH
        else:
            self.warning_level = warning_level
        super().__init__(self.warning_level)

    def before_test(self):
        """Call before each test."""
        pass

    def after_test(self):
        """Call after each test."""
        pass

    def setup(self):
        """Call before first test."""
        pass

    def finish(self):
        """Call after last test."""
        pass

    def run_tests(self):
        self._assembly()
        self.setup()
        methods = inspect.getmembers(self, predicate=inspect.ismethod)  # Get all methods of Test class
        methods = [method[0] for method in methods if method[0][0:5] == "test_"]  # Get user defined methods
        for method in methods:
            self.before_test()

            print_color("Running {}...".format(method), Style.CYAN)  # Print current test name

            iter_time = -time.process_time()
            eval("self.{}()".format(method))  # Evaluate each method
            iter_time += time.process_time()

            print_color("{:.3f} seconds\n".format(iter_time), Style.CYAN)  # Print current test run time

            self.proc_time += iter_time  # Add current test run time to total process time
            self.after_test()
        self.finish()
        time.sleep(0.01)  # Ensure dissassembly outputs last
        self._disassembly()


class Handler:
    class TestFailure(Exception):
        def __init__(self, message):
            super().__init__(message)

    class ForcedFailure(TestFailure):
        def __init__(self, message):
            super().__init__(message)

    class TestError(Exception):
        def __init__(self, message):
            super().__init__(message)

    class ComparisonError(TestError):
        def __init__(self, message):
            super().__init__(message)

    class NotEqualFailure(TestFailure):
        def __init__(self, first, second, message=None):
            if message is None:
                message = "{}: {} != {}".format(self.__class__.__name__, first, second)
            super().__init__(message)
            self.first = first
            self.second = second

    class NotComparableError(ComparisonError):
        def __init__(self, first, second, message=None):
            if message is None:
                message = "{}: types '{}' and '{}' not comparable".format(
                    self.__class__.__name__, type(first).__name__, type(second).__name__)
            super().__init__(message)
            self.first = first
            self.second = second


class Style(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


class WarningLevels(Enum):
    NONE, LOW, HIGH = range(3)

    def __ge__(self, other):
        if self.value >= other.value:
            return True
        return False


def handle_unsuccess(ef, warning_level, test_name=None):
    if warning_level == WarningLevels.HIGH:
        stacksummary = [traceback.extract_stack()[-3]]  # Get third to last traceback (last two will be in this file)
        traceback.print_list(stacksummary)
    if warning_level >= WarningLevels.LOW:
        if test_name is None:
            test_name = inspect.getouterframes(inspect.currentframe())[2][3]
        print("\t{} -> {}\n".format(test_name, ef.args[0]), file=sys.stderr)


def make_fail(reason):  # Decorator
    def factory(func):
        def test_wrapper(self):
            self.num_failed += 1
            test_name = func.__name__
            print_color("\t{} -> Forced failure: {}".format(test_name, reason), Style.RED)

        return test_wrapper

    return factory


def make_succeed(reason):  # Decorator
    def factory(func):
        def test_wrapper(self):
            self.num_successful += 1
            test_name = func.__name__
            print_color("\t{} -> Forced success: {}".format(test_name, reason), Style.GREEN)
            return True

        return test_wrapper

    return factory


def skip(reason):  # Decorator
    def factory(func):
        def test_wrapper(self):
            self.num_skipped += 1
            test_name = func.__name__
            print_color("\t{} -> Forced skip: {}".format(test_name, reason), Style.YELLOW)
            return False

        return test_wrapper

    return factory


def skip_if(condition: bool, reason):  # Decorator
    def factory(func):
        def test_wrapper(self):
            self.num_skipped += 1
            test_name = func.__name__
            print_color("\t{} -> Forced skip: {}".format(test_name, reason), Style.YELLOW)
            return False

        if condition:
            return test_wrapper

    return factory


def print_color(text, color):  # TODO: Test functionality on Windows OS
    if sys.platform.lower() == "win32":
        os.system('color')
    print(color.value + text + Style.RESET.value)
