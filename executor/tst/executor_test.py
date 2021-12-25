import os
import unittest
from typing import Optional

from src.compiled_language import CompiledLanguage
from src.interpreted_language import InterpretedLanguage
from src.config import Config
from src.executor import Executor, RunResult

all_good_stdout = "all good !"
not_good_stderr = "not good !"


class AlwaysOkLanguage(CompiledLanguage):
    def __init__(self):
        super().__init__("/usr/bin/true", ".asd", True, "/usr/bin/true")
        self.__config = Config()
        self.__output_file_path = os.path.join(self.__config.work_dir_root, "a.out")

    def compile(self, code_path: str) -> tuple:
        return all_good_stdout, "", 0

    def execute(self, code_path: str, stdin_path: Optional[str] = None) -> tuple:
        return all_good_stdout, "", 0

    def lint(self, code_path) -> tuple:
        return all_good_stdout, "", 0


class AlwaysNOkLanguage(CompiledLanguage):
    def __init__(self):
        super().__init__("/usr/bin/true", ".asd", True, "/usr/bin/true")
        self.__config = Config()
        self.__output_file_path = os.path.join(self.__config.work_dir_root, "a.out")

    def compile(self, code_path: str) -> tuple:
        return "", not_good_stderr, 123

    def execute(self, code_path: str, stdin_path: Optional[str] = None) -> tuple:
        return "", not_good_stderr, 123

    def lint(self, code_path) -> tuple:
        return "", not_good_stderr, 123


class RepeatStdinLanguage(CompiledLanguage):
    def __init__(self):
        super().__init__("/usr/bin/true", ".asd", False, "/usr/bin/true")
        self.__config = Config()
        self.__output_file_path = os.path.join(self.__config.work_dir_root, "a.out")

    def execute(self, code_path: str, stdin_path: Optional[str] = None) -> tuple:
        if stdin_path is None:
            return all_good_stdout, "", 0

        with open(stdin_path) as fp:
            return fp.read(), "", 0

    def lint(self, code_path) -> tuple:
        return all_good_stdout, "", 0


class ExecutorTest(unittest.TestCase):
    def test_01_run_valid_code(self):
        executor = Executor(AlwaysOkLanguage())

        result: RunResult = executor.run("some_test_code")

        self.assertEqual(result.stdout, all_good_stdout)
        self.assertEqual(result.stderr, "")
        self.assertEqual(result.return_code, 0)

    def test_02_run_invalid_code(self):
        executor = Executor(AlwaysNOkLanguage())

        result: RunResult = executor.run("some_test_code")

        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, not_good_stderr)
        self.assertEqual(result.return_code, 123)

    def test_03_run_test_no_stdin_no_stdout(self):
        executor = Executor(RepeatStdinLanguage())

        run_result, test_result = executor.run_test("asd")

        self.assertEqual(run_result.stdout, all_good_stdout)
        self.assertEqual(run_result.stderr, "")
        self.assertEqual(run_result.return_code, 0)

        self.assertTrue(test_result is None)

    def test_04_run_test_stdin_no_stdout(self):
        executor = Executor(RepeatStdinLanguage())

        run_result, test_result = executor.run_test("asd", stdin="some random stdin")

        self.assertEqual(run_result.stdout, "some random stdin")
        self.assertEqual(run_result.stderr, "")
        self.assertEqual(run_result.return_code, 0)

        self.assertTrue(test_result is None)

    def test_05_run_test_no_stdin_correct_stdout(self):
        executor = Executor(RepeatStdinLanguage())

        run_result, test_result = executor.run_test("asd", stdout=all_good_stdout)

        self.assertEqual(run_result.stdout, all_good_stdout)
        self.assertEqual(run_result.stderr, "")
        self.assertEqual(run_result.return_code, 0)

        self.assertTrue(test_result is not None)
        self.assertTrue(test_result.is_okay)

    def test_06_run_test_no_stdin_incorrect_stdout(self):
        executor = Executor(RepeatStdinLanguage())

        run_result, test_result = executor.run_test("asd", stdout=not_good_stderr)

        self.assertEqual(run_result.stdout, all_good_stdout)
        self.assertEqual(run_result.stderr, "")
        self.assertEqual(run_result.return_code, 0)

        self.assertTrue(test_result is not None)
        self.assertFalse(test_result.is_okay)
        self.assertTrue(len(test_result.diff) > 0)

    def test_07_run_test_stdin_correct_stdout(self):
        executor = Executor(RepeatStdinLanguage())

        test_string = 'The answer is 42'
        run_result, test_result = executor.run_test("asd", stdin=test_string, stdout=test_string)

        self.assertEqual(run_result.stdout, test_string)
        self.assertEqual(run_result.stderr, "")
        self.assertEqual(run_result.return_code, 0)

        self.assertTrue(test_result is not None)
        self.assertTrue(test_result.is_okay)

    def test_08_run_test_stdin_incorrect_stdout(self):
        executor = Executor(RepeatStdinLanguage())

        test_string = 'The answer is 42'
        run_result, test_result = executor.run_test("asd", stdin=test_string,
                                                    stdout=test_string + "!")

        self.assertEqual(run_result.stdout, test_string)
        self.assertEqual(run_result.stderr, "")
        self.assertEqual(run_result.return_code, 0)

        self.assertTrue(test_result is not None)
        self.assertFalse(test_result.is_okay)
        self.assertTrue(len(test_result.diff) > 0)


if __name__ == '__main__':
    unittest.main()
