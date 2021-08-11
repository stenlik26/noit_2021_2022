import os

from compiled_language import CompiledLanguage
from src.config import Config


class CppLanguage(CompiledLanguage):
    def __init__(self, executable: str, file_extension: str, is_compiled: bool):
        super().__init__(executable, file_extension, is_compiled)
        self.__config = Config()
        self.__output_file_path = os.path.join(self.__config.work_dir_root, "a.out")

    def compile(self, code_path: str) -> tuple:
        return super().execute_command(self.executable, [code_path, "-o", self.__output_file_path])

    def execute(self, code_path) -> tuple:
        out, err, return_code = self.compile(code_path)

        if return_code == 0:
            return super().execute_command(self.__output_file_path)

        return out, err, return_code
