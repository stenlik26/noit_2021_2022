from src.python import PythonLanguage
from src.cpp import CppLanguage
from src.java import JavaLanguage
from src.csharp import CsharpLanguage
from src.executor import Executor


class LanguageExecutors:
    def __init__(self):
        self.__python_lang = PythonLanguage("/usr/bin/python3", '.py', False, "/usr/bin/pylint")
        self.__cpp_lang = CppLanguage("/usr/bin/g++", '.cpp', True, '/usr/bin/clang-tidy')
        self.__java_lang = JavaLanguage("/usr/bin/javac", '.java', True,  'java -jar checkstyle-9.2.1-all.jar {} -c google_checks.xml')
        self.__csharp_lang = CsharpLanguage('/usr/bin/dotnet', '.cs', True, '')
        self.__executorPy = Executor(self.__python_lang)
        self.__executorCpp = Executor(self.__cpp_lang)
        self.__executorJava = Executor(self.__java_lang)
        self.__executorCsharp = Executor(self.__csharp_lang)

    def get_executor(self, language: str) -> Executor:
        if language == 'python':
            return self.__executorPy
        elif language == 'cpp':
            return self.__executorCpp
        elif language == 'java':
            return self.__executorJava
        elif language == 'csharp':
            return self.__executorCsharp
