import os
from language_information import Language
from config import Config


class Executor:
    def __init__(self, language: Language):
        self.__language = language
        self.__config = Config()

    def run(self, code: str) -> tuple:
        path = self.__save_code_to_file(code)

        if path != "":
            return self.__language.execute(path)
        else:
            print("Can't execute")
            return ()

    def lint(self, code: str) -> tuple:
        path = self.__save_code_to_file(code)

        if path != "":
            return self.__language.lint(path)
        else:
            print("Can't execute")
            return ()

    def __save_code_to_file(self, code: str) -> str:
        if not os.path.exists(self.__config.work_dir_root):
            os.mkdir(self.__config.work_dir_root)

        code_path = self.__generate_file_path()

        with open(code_path, 'w') as f:
            try:
                f.write(code)
            except IOError as err:
                print("IO error caught: {}".format(err))
                return ""

        return code_path

    def __generate_file_path(self) -> str:
        return os.path.join(self.__config.work_dir_root, self.__generate_file_name())

    def __generate_file_name(self) -> str:
        # TODO - Add session id to file name
        return "code" + self.__language.file_extension
