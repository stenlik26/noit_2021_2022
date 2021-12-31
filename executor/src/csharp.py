import os
from typing import Optional

from src.compiled_language import CompiledLanguage
from src.config import Config


class CsharpLanguage(CompiledLanguage):
    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        super().__init__(executable, file_extension, is_compiled, linter)
        self.__config = Config()

    def compile(self, code_path: str) -> tuple:
        return super().execute_command(self.executable, ['build', code_path])

    def execute(self, code_path: str, stdin_path: Optional[str] = None, timeout: float = 10) -> tuple:
        out, err, return_code = self.compile(code_path)

        if return_code == 0:
            return super().execute_command(self.executable, ['run', '--project', code_path], stdin_path, timeout)

        return out, err, return_code

    def lint(self, code_path):
        print('No csharp linter implemented')
        return None
