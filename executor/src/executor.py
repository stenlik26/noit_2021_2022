import os
from typing import Optional

from language_information import Language
from config import Config
import csharp


class RunResult:
    def __init__(self, output: tuple):
        self.stdout = output[0]
        self.stderr = output[1]
        self.return_code = output[2]

    def to_dict(self) -> dict:
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "return_code": self.return_code
        }


class TestResult:
    def __init__(self, is_okay: bool, diff: str):
        self.is_okay = is_okay
        self.diff = diff

    def to_dict(self) -> dict:
        return {
            "is_passing": self.is_okay,
            "diff": self.diff,
        }


class Executor:
    def __init__(self, language: Language):
        self.__language = language
        self.__config = Config()

    def run(self, code: str) -> RunResult:
        path = self.__save_code_to_file(code)

        if path != "":
            return RunResult(self.__language.execute(path))
        else:
            return RunResult(("", "Can't execute", 1))

    def run_test(self, code: str, stdin: Optional[str], stdout: Optional[str]) -> (RunResult, Optional[TestResult]):
        path = self.__save_code_to_file(code)

        stdin_path = None
        if stdin is not None:
            stdin_path = self.__create_file(stdin, "stdin.txt")

        stdout_path = None
        if stdout is not None:
            stdout_path = self.__create_file(stdout,  "stdout.txt")

        if path != "":
            run_result = RunResult(self.__language.execute(path, stdin_path))

            if stdout_path is not None:
                output_path = self.__create_file(run_result.stdout, "output.txt")
                test_result = self.__compare_outputs(output_path, stdout_path)

                return run_result, test_result
            else:
                return run_result, None
        else:
            return RunResult(("", "Can't execute", 1)), None

    def lint(self, code: str) -> RunResult:
        path = self.__save_code_to_file(code)

        if path != "":
            return RunResult(self.__language.lint(path))
        else:
            return RunResult(("", "Can't execute", 1))

    def __save_code_to_file(self, code: str) -> str:
        if not os.path.exists(self.__config.work_dir_root):
            os.mkdir(self.__config.work_dir_root)

        if type(self.__language) == csharp.CsharpLanguage:

            csharp_path = os.path.join(self.__config.work_dir_root,
                                       self.__generate_csharp_project_folder())

            if not os.path.exists(csharp_path):
                os.mkdir(csharp_path)

            self.__language.execute_command('dotnet', ['new', 'console', '-o', csharp_path])

            code_path = self.__create_file(code, os.path.join(csharp_path, 'Program.cs'))
            code_path = code_path.replace('/Program.cs', '')
        else:
            code_path = self.__create_file(code, self.__generate_file_path())

        return code_path

    def __create_file(self, content: str, file_name: str, dir_path: str = "") -> str:
        if dir_path == "":
            dir_path = self.__config.work_dir_root

        file_path = os.path.join(dir_path, file_name)

        with open(file_path, 'w') as f:
            try:
                f.write(content)
            except IOError as err:
                print("IO error caught: {}".format(err))
                return ""

        return file_path

    def __generate_file_path(self) -> str:
        return os.path.join(self.__config.work_dir_root, self.__generate_file_name())

    def __generate_file_name(self) -> str:
        # TODO - Add session id to file name
        return "code" + self.__language.file_extension

    def __generate_csharp_project_folder(self) -> str:
        # TODO - Think about this
        return "project1"

    def __compare_outputs(self, program_output_path: str, expected_output_path: str) -> TestResult:
        # TODO - This is not ideal - consider moving `execute_command` somewhere else
        stdout, _, rc = self.__language.execute_command("diff",
                                                        ["-y", program_output_path, expected_output_path])

        return TestResult(rc == 0, stdout)
