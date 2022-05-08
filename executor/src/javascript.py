from typing import Optional

from src.interpreted_language import InterpretedLanguage


class JavaScriptLanguage(InterpretedLanguage):

    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        super().__init__(executable, file_extension, is_compiled, linter)

    def execute(self, code_path: str, stdin_path: Optional[str] = None, timeout: float = 2) -> tuple:
        return super().execute_command(self.executable, [code_path], stdin_path, timeout)

    def lint(self, code_path) -> tuple:
        return "Not implemented", "Not implemented"
