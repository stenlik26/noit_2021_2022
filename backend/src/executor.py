import os
from language_information import Language

DEFAULT_PATH = '/tmp/code'


class Executor:
    def __init__(self, language: Language):
        self.__language = language

    def run(self, code: str) -> tuple:
        path = self.__save_code_to_file(code)

        if path != "":
            return self.__language.execute(path)
        else:
            print("Can't execute")
            return ()

    def __save_code_to_file(self, code: str) -> str:
        if not os.path.exists(DEFAULT_PATH):
            os.mkdir(DEFAULT_PATH)

        code_path = self.__generate_file_path()

        with open(code_path, 'w') as f:
            try:
                f.write(code)
            except IOError as err:
                print("IO error caught: {}".format(err))
                return ""

        return code_path

    def __generate_file_path(self) -> str:
        return os.path.join(DEFAULT_PATH, self.__generate_file_name())

    def __generate_file_name(self) -> str:
        return "code" + self.__language.file_extension
