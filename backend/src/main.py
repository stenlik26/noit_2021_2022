from python import PythonLanguage
from src.cpp import CppLanguage
from src.executor import Executor

if __name__ == "__main__":
    python_lang = PythonLanguage("/usr/bin/python3", '.py', False)
    cpp_lang = CppLanguage("/usr/bin/g++", '.cpp', False)
    executor = Executor(cpp_lang)

    #out, err, rc = executor.run("print('Hello from Python')")
    out, err, rc = executor.run('#include <iostream>\nint main(){\nstd::cout<<"Hello from C++\\n";\nreturn 0;\n}')
    print("Out = {}\nErr = {}\nrc = {}\n".format(out, err, rc))
