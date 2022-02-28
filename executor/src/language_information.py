from abc import ABC
import subprocess
from typing import Optional


class Language(ABC):
    def __init__(self, executable: str, file_extension: str, is_compiled: bool, linter: str):
        self.__file_extension = file_extension
        self.__is_compiled = is_compiled
        self.__executable = executable
        self.__linter = linter

    @property
    def file_extension(self) -> str:
        return self.__file_extension

    @property
    def is_compiled(self) -> bool:
        return self.__is_compiled

    @property
    def executable(self) -> str:
        return self.__executable

    @property
    def linter(self) -> str:
        return self.__linter

    @staticmethod
    def execute_command(command: str, args: list, stdin_path: Optional[str] = None, timeout: float = 2) -> tuple:

        stdin = subprocess.PIPE if stdin_path is None else open(stdin_path)
        full_command = [command] + args
        try:
            result = subprocess.run(full_command, text=True,
                                stdin=stdin,
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                timeout=timeout)
        except subprocess.TimeoutExpired as timeout_error:
            return f"Изпълненият тест надвиши времевия лимит от {timeout} секунди", timeout_error.stderr, 1
        except Exception as ex:
            return f"Unknown exception caught {ex}", "", 1

        if stdin_path is not None:
            stdin.close()
        return result.stdout.strip(), result.stderr, result.returncode

    def execute(self, code_path: str, stdin_path: Optional[str] = None, timeout: float = 2) -> tuple:
        pass

    def lint(self, code_path) -> tuple:
        pass
