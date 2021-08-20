from python import PythonLanguage
from cpp import CppLanguage
from java import JavaLanguage
from executor import Executor


class LanguageExecutors:
    def __init__(self):
        self.__python_lang = PythonLanguage("/usr/bin/python3", '.py', False, "/usr/bin/pylint")
        self.__cpp_lang = CppLanguage("/usr/bin/g++", '.cpp', True, '/usr/bin/clang-tidy')
        self.__java_lang = JavaLanguage("/usr/bin/javac", '.java', True, '')
        self.__executorPy = Executor(self.__python_lang)
        self.__executorCpp = Executor(self.__cpp_lang)
        self.__executorJava = Executor(self.__java_lang)

    def get_executor(self, language: str) -> Executor:
        if language == 'python':
            return self.__executorPy
        elif language == 'cpp':
            return self.__executorCpp
        elif language == 'java':
            return self.__executorJava
