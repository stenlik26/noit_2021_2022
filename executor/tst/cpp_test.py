import os.path
import unittest

from typing import List
from src.config import Config
from src.cpp import CppLanguage


class CppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.compiler = '/usr/bin/g++'
        cls.extension = '.cpp'
        cls.is_compiled = True
        cls.linter = '/usr/bin/clang-tidy'
        cls.config = Config()

        if not os.path.exists(cls.config.work_dir_root):
            os.makedirs(cls.config.work_dir_root, exist_ok=True)

        cls.valid_code_lines = [
            '#include <iostream>\n',
            '\n',
            'int main() {\n',
            '\t//Program that prints "Hello world" to the console\n',
            '\tstd::cout<<"Hello world"<<std::endl;\n',
            '\treturn 0;\n',
            '}\n',
        ]

        cls.invalid_code_lines = [
                '#include <iostream>\n',
                '\n',
                'int main() {\n',
                '\t//Program that prints "Hello world" to the console\n',
                '\tstd::cout<<"Hello world"<<std::endl\n',
                '\treturn 0;\n',
                '}\n'
            ]

        cls.tmp_cpp_file_path = os.path.join('/tmp', 'sample.cpp')
        cls.cpp = CppLanguage(cls.compiler, cls.extension, cls.is_compiled,
                              cls.linter)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.config.work_dir_root):
            for dirname, dirs, files in os.walk(cls.config.work_dir_root):
                for file in files:
                    os.remove(os.path.join(dirname, file ))

            os.rmdir(cls.config.work_dir_root)

    def tearDown(self) -> None:
        if os.path.exists(self.tmp_cpp_file_path):
            os.remove(self.tmp_cpp_file_path)

    def test_01_compile_valid_code(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.cpp.compile(self.tmp_cpp_file_path)

        self.assertEqual(result[1], "")
        self.assertEqual(result[2], 0)

    def test_02_compile_invalid_code(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.cpp.compile(self.tmp_cpp_file_path)

        self.assertNotEqual(result[1], "")
        self.assertNotEqual(result[2], 0)

    def test_03_execute_valid_code_no_stdin(self):
        self.__write_to_tmp_file(self.valid_code_lines)

        result = self.cpp.execute(self.tmp_cpp_file_path)

        self.assertEqual(result[0], "Hello world\n")
        self.assertEqual(result[2], 0)

    def test_04_execute_valid_code_with_stdin(self):
        cpp_lines = [
            '#include <iostream>\n',
            '\n',
            'int main() {\n',
            '\t//Program that prints "Hello world" to the console\n',
            '\tint a = 0;\n',
            '\tstd::cin >> a;\n',
            '\tint b = 0;\n',
            '\tstd::cin >> b;\n',
            '\tstd::cout<<a+b<<std::endl;\n',
            '\treturn 0;\n',
            '}\n',
        ]
        self.__write_to_tmp_file(cpp_lines)

        stdin_content = "3\n5\n";
        stdin_path = os.path.join("/tmp", "test_03_stdin.txt")
        with open(stdin_path, 'w+') as fp:
            fp.write(stdin_content)

        result = self.cpp.execute(self.tmp_cpp_file_path, stdin_path)

        os.remove(stdin_path)
        self.assertEqual(result[0], "8\n")
        self.assertEqual(result[2], 0)

    def test_05_execute_invalid(self):
        self.__write_to_tmp_file(self.invalid_code_lines)

        result = self.cpp.execute(self.tmp_cpp_file_path)

        self.assertNotEqual(result[1], "")
        self.assertNotEqual(result[2], 0)

    def __write_to_tmp_file(self, content: List[str]):
        with open(self.tmp_cpp_file_path, 'w+') as fp:
            fp.writelines(content)


if __name__ == '__main__':
    unittest.main()
