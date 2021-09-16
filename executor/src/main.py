from flask import Flask, request, jsonify
import flask_cors
from language_executors import LanguageExecutors
app = Flask(__name__)
flask_cors.CORS(app)

language_executors = LanguageExecutors()


@app.route('/lint', methods=['POST'])
def lint_code():
    post_info = request.get_json()
    # TODO: Check if all params are given / valid. Decorator?
    executor = language_executors.get_executor(post_info['language'])

    out_lint, err_lint, rc_lint = executor.lint(post_info['code'])

    return jsonify({
        "status": "OK",
        "message": {
            "stdout": out_lint,
            "stderr": err_lint,
            "return_code": rc_lint
        }})


@app.route('/run_code', methods=['POST'])
def run_code():
    post_info = request.get_json()
    # TODO: Check if all params are given / valid. Decorator?
    executor = language_executors.get_executor(post_info['language'])

    out_run, err_run, rc_run = executor.run(post_info['code'])

    return jsonify({
        "status": "OK",
        "message": {
            "stdout": out_run,
            "stderr": err_run,
            "return_code": rc_run
        }})


@app.route('/')
def debug_page():
    return 'This is the debug page for the executor api. (API works)'


if __name__ == "__main__":



    '''
    outPy, errPy, rcPy = executorPy.run("print('Hello from Python')")
    outLint, errLint, rcLint = executorPy.lint("print('Hello from Python')")

    executorCpp.lint('#include <iostream>\nint main(){\nstd::cout<<"Hello from C++\\n";\nreturn 0;\n}')

    outCpp, errCpp, rcCpp = executorCpp.run('#include <iostream>\nint main(){\nstd::cout<<"Hello from C++\\n";\nreturn 0;\n}')

    print("Out = {}Err = {}\nrc = {}\n".format(outPy, errPy, rcPy))
    print("Pylint Out = {}Pylint Err = {}\nPylint rc = {}\n".format(outLint, errLint, rcLint))
    print("Cpp Out = {}Cpp Err = {}\nCpp rc = {}\n".format(outCpp, errCpp, rcCpp))
    
    '''

    #executor = language_executors.get_executor('csharp')

    #out_run, err_run, rc_run = executor.run('using System;public class TestProgram{public static void Main(){Console.WriteLine("Hello World");}}')

    app.run()
