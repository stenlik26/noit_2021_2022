import os
import re

from compiled_language import CompiledLanguage
from config import Config


class JavaLanguage(CompiledLanguage):
    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        super().__init__(executable, file_extension, is_compiled, linter)
        self.__config = Config()

    def compile(self, code_path: str) -> tuple:
        return super().execute_command(self.executable, [code_path])

    def execute(self, code_path) -> tuple:
        out, err, return_code = self.compile(code_path)

        with open(code_path, 'r') as file:
            code = file.read()

        compiled_name = re.search('class ([a-zA-Z_0-9-]*)', code)
        compiled_name = compiled_name.group()
        compiled_name = compiled_name.replace('class ', '')

        if return_code == 0:
            return super().execute_command('java', ['-cp', self.__config.work_dir_root, compiled_name])

        return out, err, return_code

    def lint(self, code_path):
        print('No java linter implemented')
        return None
