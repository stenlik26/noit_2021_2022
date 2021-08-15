from interpreted_language import InterpretedLanguage


class PythonLanguage(InterpretedLanguage):

    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        super().__init__(executable, file_extension, is_compiled)
        self.linter = linter

    def execute(self, code_path) -> tuple:
        return super().execute_command(self.executable, [code_path])

    def run_linter(self, code_path) -> tuple:
        return super().execute_command(self.linter, [code_path])
