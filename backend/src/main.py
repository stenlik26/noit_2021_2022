from language_information import Language
from python import PythonLanguage

if __name__ == "__main__":
    inst = PythonLanguage("python", "python", '.py', False)

    print(inst.execute('test.py'))
    print("Hello world")
