from abc import ABC
import subprocess


class Language(ABC):
    def __init__(self, name: str, executable: str, file_extension: str, is_compiled: bool):
        self.__name = name
        self.__file_extension = file_extension
        self.__is_compiled = is_compiled
        self.__executable = executable

    @property
    def name(self) -> str:
        return self.__name

    @property
    def file_extension(self) -> str:
        return self.__file_extension

    @property
    def is_compiled(self) -> bool:
        return self.__is_compiled

    @property
    def executable(self) -> str:
        return self.__executable

    @staticmethod
    def execute_command(command: str, args: list[str]) -> tuple:
        full_command = [command] + args
        result = subprocess.run(full_command, shell=True, text=True,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        return result.stdout, result.stderr, result.returncode

    def execute(self, code_path) -> tuple:
        pass

