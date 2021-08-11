from python import PythonLanguage
from src.executor import Executor

if __name__ == "__main__":
    python_lang = PythonLanguage("python3", '.py', False)
    executor = Executor(python_lang)

    out, err, rc = executor.run("print('Hello from Python')")
    print("Out = {}\nErr = {}\nrc = {}\n".format(out, err, rc))
