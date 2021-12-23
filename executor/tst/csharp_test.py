import os.path
import subprocess
import unittest

from typing import List
from src.config import Config
from src.csharp import CsharpLanguage


class CsharpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compiler = '/usr/bin/dotnet'
        cls.extension = '.cs'
        cls.is_compiled = True
        cls.linter = ''
        cls.config = Config(os.path.join('/tmp', 'cs'))

        if not os.path.exists(cls.config.work_dir_root):
            os.makedirs(cls.config.work_dir_root, exist_ok=True)

        cls.valid_code_lines = [
            'using System;\n',
            '\n',
            'namespace cs\n',
            '{\n',
            '\tclass Program\n',
            '\t{\n',
            '\t\tstatic void Main(string[] args)\n',
            '\t\t{\n',
            '\t\t\tConsole.WriteLine("Hello world");\n',
            '\t\t}\n',
            '\t}\n',
            '}\n',
        ]

        cls.invalid_code_lines = [
            'using System;\n',
            '\n',
            'namespace cs\n',
            '{\n',
            '\tclass Program\n',
            '\t\tstatic void Main(string[] args)\n',
            '\t\t{\n',
            '\t\t\tConsole.WriteLine("Hello world")\n',
            '\t\t}\n',
            '\t}\n',
            '}\n',
        ]

        subprocess.run(['dotnet', 'new', 'console', '-o', cls.config.work_dir_root])

        cls.tmp_cs_file_path = os.path.join(cls.config.work_dir_root, 'Program.cs')
        cls.csharp = CsharpLanguage(cls.compiler, cls.extension, cls.is_compiled,
                                    cls.linter)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.config.work_dir_root):
            subprocess.run(["rm", "-rf" , f"{cls.config.work_dir_root}"])

    def test_01_compile_valid_code(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.csharp.compile(self.config.work_dir_root)

        self.assertEqual(result[1], "")
        self.assertEqual(result[2], 0)

    def test_02_compile_invalid_code(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.csharp.compile(self.config.work_dir_root)

        self.assertNotEqual(result[0], "")
        self.assertNotEqual(result[2], 0)

    def test_03_execute_valid_code_no_stdin(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.csharp.execute(self.config.work_dir_root)

        self.assertEqual(result[0].strip(), "Hello world")
        self.assertEqual(result[2], 0)

    def test_04_execute_valid_code_with_stdin(self):
        csharp_lines = [
            'using System;\n',
            '\n',
            'namespace cs\n',
            '{\n',
            '\tclass Program\n',
            '\t{\n',
            '\t\tstatic void Main(string[] args)\n',
            '\t\t{\n',
            '\t\t\tint a = Convert.ToInt32( Console.ReadLine());\n'
            '\t\t\tint b = Convert.ToInt32( Console.ReadLine());\n'
            '\t\t\tConsole.WriteLine(a+b);\n',
            '\t\t}\n',
            '\t}\n',
            '}\n',
        ]
        self.__write_to_tmp_file(csharp_lines)

        stdin_content = "3\n5\n"
        stdin_path = os.path.join("/tmp", "test_03_stdin.txt")
        with open(stdin_path, 'w+') as fp:
            fp.write(stdin_content)

        result = self.csharp.execute(self.config.work_dir_root, stdin_path)

        os.remove(stdin_path)
        self.assertEqual(result[0], "8\n")
        self.assertEqual(result[2], 0)

    def test_05_execute_invalid(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.csharp.execute(self.config.work_dir_root)

        self.assertNotEqual(result[0], "")
        self.assertNotEqual(result[2], 0)

    def test_06_lint_valid_code(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.csharp.lint(self.config.work_dir_root)

        self.assertEqual(result[2], 0)

    def __write_to_tmp_file(self, content: List[str]):
        with open(self.tmp_cs_file_path, 'w+') as fp:
            fp.writelines(content)

    def __setup_csharp_project(self):
        subprocess.run(['dotnet', 'new', 'console', '-o', self.config.work_dir_root])


if __name__ == '__main__':
    unittest.main()
