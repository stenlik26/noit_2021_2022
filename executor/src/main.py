from python import PythonLanguage
from cpp import CppLanguage
from executor import Executor
if __name__ == "__main__":
    python_lang = PythonLanguage("/usr/bin/python3", '.py', False, "/usr/bin/pylint")
    cpp_lang = CppLanguage("/usr/bin/g++", '.cpp', False, "")
    executorPy = Executor(python_lang)
    executorCpp = Executor(cpp_lang)

    outPy, errPy, rcPy = executorPy.run("print('Hello from Python')")
    outLint, errLint, rcLint = executorPy.lint("print('Hello from Python')")

    executorCpp.lint('#include <iostream>\nint main(){\nstd::cout<<"Hello from C++\\n";\nreturn 0;\n}')

    outCpp, errCpp, rcCpp = executorCpp.run('#include <iostream>\nint main(){\nstd::cout<<"Hello from C++\\n";\nreturn 0;\n}')

    print("Out = {}Err = {}\nrc = {}\n".format(outPy, errPy, rcPy))
    print("Pylint Out = {}Pylint Err = {}\nPylint rc = {}\n".format(outLint, errLint, rcLint))
    print("Cpp Out = {}Cpp Err = {}\nCpp rc = {}\n".format(outCpp, errCpp, rcCpp))
