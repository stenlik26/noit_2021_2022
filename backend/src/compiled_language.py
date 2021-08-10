from language_information import Language


class CompiledLanguage(Language):

    def __init__(self,  name: str, executable: str, file_extension: str, is_compiled: bool):
        super().__init__(name, executable, file_extension, is_compiled)

    def compile(self, code_path: str) -> tuple:
        pass
