from typing import Optional

from interpreted_language import InterpretedLanguage


class PythonLanguage(InterpretedLanguage):

    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        super().__init__(executable, file_extension, is_compiled, linter)

    def execute(self, code_path: str, stdin_path: Optional[str] = None) -> tuple:
        return super().execute_command(self.executable, [code_path], stdin_path)

    def lint(self, code_path) -> tuple:
        return super().execute_command(self.linter, [code_path])
