import os.path
import unittest

from typing import List
from src.config import Config
from src.python import PythonLanguage


class JavaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compiler = '/usr/bin/python3'
        cls.extension = '.py'
        cls.is_compiled = False
        cls.linter = '/usr/bin/pylint'
        cls.config = Config()

        if not os.path.exists(cls.config.work_dir_root):
            os.makedirs(cls.config.work_dir_root, exist_ok=True)

        cls.valid_code_lines = [
            'print("Hello world")\n'
        ]

        cls.invalid_code_lines = [
            'print("hello world"\n'
        ]

        cls.tmp_python_file_path = os.path.join(cls.config.work_dir_root, 'sample.py')
        cls.python = PythonLanguage(cls.compiler, cls.extension, cls.is_compiled,
                                    cls.linter)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.config.work_dir_root):
            for dirname, dirs, files in os.walk(cls.config.work_dir_root):
                for file in files:
                    os.remove(os.path.join(dirname, file ))

            os.rmdir(cls.config.work_dir_root)

    def tearDown(self) -> None:
        if os.path.exists(self.tmp_python_file_path):
            os.remove(self.tmp_python_file_path)

    def test_01_execute_valid_code_no_stdin(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.python.execute(self.tmp_python_file_path)

        self.assertEqual(result[0], "Hello world\n")
        self.assertEqual(result[2], 0)

    def test_02_execute_valid_code_with_stdin(self):
        python_lines = [
            'a = int(input())\n',
            'b = int(input())\n',
            'print(a+b)'
        ]

        self.__write_to_tmp_file(python_lines)

        stdin_content = "3\n5\n"
        stdin_path = os.path.join("/tmp", "test_03_stdin.txt")
        with open(stdin_path, 'w+') as fp:
            fp.write(stdin_content)

        result = self.python.execute(self.tmp_python_file_path, stdin_path)

        os.remove(stdin_path)
        self.assertEqual(result[0], "8\n")
        self.assertEqual(result[2], 0)

    def test_03_execute_invalid(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.python.execute(self.tmp_python_file_path)

        self.assertNotEqual(result[1], "")
        self.assertNotEqual(result[2], 0)

    def test_04_lint_valid_code(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.python.lint(self.tmp_python_file_path)

        self.assertEqual(result[2], 0)

    def __write_to_tmp_file(self, content: List[str]):
        with open(self.tmp_python_file_path, 'w+') as fp:
            fp.writelines(content)


if __name__ == '__main__':
    unittest.main()
