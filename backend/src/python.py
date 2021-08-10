from interpreted_language import InterpretedLanguage


class PythonLanguage(InterpretedLanguage):

    def __init__(self, name: str, executable: str, file_extension: str, is_compiled: bool):
        super().__init__(name, executable, file_extension, is_compiled)

    def execute(self, code_path) -> tuple:
        return super().execute_command(self.executable, [code_path])