from flask import Flask, request, jsonify
import flask_cors
from language_executors import LanguageExecutors
from src.executor import RunResult, Executor

app = Flask(__name__)
flask_cors.CORS(app)

language_executors = LanguageExecutors()


@app.route('/lint', methods=['POST'])
def lint_code():
    post_info = request.get_json()
    executor: Executor = language_executors.get_executor(post_info['language'])

    result: RunResult = executor.lint(post_info['code'])

    return jsonify({
        "status": "OK",
        "message": result.to_dict()
    })


@app.route('/run_code', methods=['POST'])
def run_code():
    post_info = request.get_json()
    executor: Executor = language_executors.get_executor(post_info['language'])

    result: RunResult = executor.run_test(post_info['code'])

    return jsonify({
        "status": "OK",
        "message": result.to_dict()
    })


@app.route('/run_test', methods=['POST'])
def run_test():
    post_info = request.get_json()
    executor = language_executors.get_executor(post_info['language'])

    stdin = post_info['stdin'] if 'stdin' in post_info else None
    expected_stdout = post_info['expected_stdout'] if 'expected_stdout' in post_info else None

    run_result, test_result = executor.run_test(post_info['code'], stdin, expected_stdout)

    run_result_dict: dict = run_result.to_dict()

    if test_result is not None:
        test_result_dict: dict = test_result.to_dict()

        # This merges two dictionaries
        run_result_dict.update(test_result_dict)

    return jsonify({
        "status": "OK",
        "message": run_result_dict
    })


@app.route('/')
def debug_page():
    return 'This is the debug page for the executor api. (API works)'


if __name__ == "__main__":
    app.run()
