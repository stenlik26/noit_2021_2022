from language_information import Language


class InterpretedLanguage(Language):

    def __init__(self, name: str, executable: str, file_extension: str, is_compiled: bool):
        super().__init__(name, executable, file_extension, is_compiled)
