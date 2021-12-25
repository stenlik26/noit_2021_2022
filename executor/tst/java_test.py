import os.path
import unittest

from typing import List
from src.config import Config
from src.java import JavaLanguage


class JavaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compiler = '/usr/bin/javac'
        cls.extension = '.java'
        cls.is_compiled = True
        cls.linter = 'java -jar checkstyle-9.0.1-all.jar {} -c google_checks.xml'
        cls.config = Config()

        if not os.path.exists(cls.config.work_dir_root):
            os.makedirs(cls.config.work_dir_root, exist_ok=True)

        cls.valid_code_lines = [
            'class Main {\n',
            '\tpublic static void main(String[] args) {\n',
            '\t\tSystem.out.println("Hello world");\n',
            '\t}\n',
            '}\n',
        ]

        cls.invalid_code_lines = [
            'class Main {\n',
            '\tpublic static void main(String[] args) {\n',
            '\t\tSystem.out.println("Hello world")\n',
            '\t}\n',
            '}\n',
        ]

        cls.tmp_java_file_path = os.path.join(cls.config.work_dir_root,  'Sample.java')
        cls.java = JavaLanguage(cls.compiler, cls.extension, cls.is_compiled,
                                cls.linter)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.config.work_dir_root):
            for dirname, dirs, files in os.walk(cls.config.work_dir_root):
                for file in files:
                    os.remove(os.path.join(dirname, file ))

            os.rmdir(cls.config.work_dir_root)

    def tearDown(self) -> None:
        if os.path.exists(self.tmp_java_file_path):
            os.remove(self.tmp_java_file_path)

    def test_01_compile_valid_code(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.java.compile(self.tmp_java_file_path)

        self.assertEqual(result[1], "")
        self.assertEqual(result[2], 0)

    def test_02_compile_invalid_code(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.java.compile(self.tmp_java_file_path)

        self.assertNotEqual(result[1], "")
        self.assertNotEqual(result[2], 0)

    def test_03_execute_valid_code_no_stdin(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.java.execute(self.tmp_java_file_path)

        print(result)
        self.assertEqual(result[0], "Hello world\n")
        self.assertEqual(result[2], 0)

    def test_04_execute_valid_code_with_stdin(self):
        java_lines = [
            'import java.util.Scanner;\n',
            'class Main {\n',
            '\tpublic static void main(String[] args) {\n',
            '\t\tScanner console = new Scanner(System.in);\n',
            '\t\tint a = console.nextInt();\n',
            '\t\tint b = console.nextInt();\n',
            '\t\tSystem.out.println(a+b);\n',
            '\t}\n',
            '}\n',
        ]

        self.__write_to_tmp_file(java_lines)

        stdin_content = "3\n5\n"
        stdin_path = os.path.join("/tmp", "test_03_stdin.txt")
        with open(stdin_path, 'w+') as fp:
            fp.write(stdin_content)

        result = self.java.execute(self.tmp_java_file_path, stdin_path)

        os.remove(stdin_path)
        self.assertEqual(result[0], "8\n")
        self.assertEqual(result[2], 0)

    def test_05_execute_invalid(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.java.execute(self.tmp_java_file_path)

        self.assertNotEqual(result[1], "")
        self.assertNotEqual(result[2], 0)

    def test_06_lint_valid_code(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.java.lint(self.tmp_java_file_path)

        print(result[0])
        self.assertEqual(result[2], 0)

    def __write_to_tmp_file(self, content: List[str]):
        with open(self.tmp_java_file_path, 'w+') as fp:
            fp.writelines(content)


if __name__ == '__main__':
    unittest.main()
