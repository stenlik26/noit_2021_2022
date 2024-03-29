import os
from typing import Optional

from src.compiled_language import CompiledLanguage
from src.config import Config


class CLanguage(CompiledLanguage):
    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        super().__init__(executable, file_extension, is_compiled, linter)
        self.__config = Config()
        self.__output_file_path = os.path.join(self.__config.work_dir_root, "a.out")

    def compile(self, code_path: str) -> tuple:
        return super().execute_command(self.executable, [code_path, "-o", self.__output_file_path])

    def execute(self, code_path: str, stdin_path: Optional[str] = None,
                timeout: float = 2) -> tuple:
        out, err, return_code = self.compile(code_path)

        if return_code == 0:
            return super().execute_command(self.__output_file_path, [], stdin_path, timeout)

        return out, err, return_code

    def lint(self, code_path):
        return super().execute_command(self.linter, ['-checks="*"', code_path])
