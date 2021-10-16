from flask import Flask, request, jsonify
import flask_cors
import requests
from backend.src.mongo_connection.mongo_connection import get_executor_address
from backend.src.mongo_connection.mongo_connection import get_connection
from backend.src.register_user.register_user import RegisterUserClass
from backend.src.login_user.login_user import LoginUserClass
from backend.src.handle_problems.handle_problems import HandleProblemsClass

app = Flask(__name__)
flask_cors.CORS(app)


def is_user_valid(token: str, user_id: str) -> bool:
    # TODO: implement this
    return True


def is_guest_token_valid(token: str) -> bool:
    # TODO: implement this
    return True


def check_for_post_params(needed_params: tuple, given_params: dict) -> bool:
    """
    Функцията проверява нужните параметри съответстват с получените.
    Проверката се извършва чрез tuple от низове, които трябва да присъстват като ключове в dictionary-то.

    :param needed_params: Нужните параметри от тип tuple.
    :param given_params: Получените параметри от тип dictionary.
    :return: Връща True или False, в зависимост от това дали всички нужни параметри присъстват.
    """
    return all(key in given_params for key in needed_params)


def check_if_empty(keys_to_check: tuple, params: dict) -> bool:
    """
    Функцията проверява дали дадени полета в dictionary-то са празни.
    Ако име празни полета се връща True, ако няма False.

    :param keys_to_check: Ключове в dictionary за проверка.
    :param params: Dictionary с ключове и стойности.
    :return: Връща True или False в зависимост от това дали има празни полета в dictionary-то.
    """
    for x in keys_to_check:
        if not params[x]:
            return True
    return False


@app.route('/run_code', methods=['POST'])
def run_code():
    post_info = request.get_json()

    if not check_for_post_params(('user_id', 'code', 'language', 'token'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    url = get_executor_address() + '/run_code'

    inputParams = {
        'language': post_info['language'],
        'code': post_info['code']
    }

    result = requests.post(url=url, json=inputParams)

    data = result.json()

    return jsonify({'status': 'OK', 'message': data})


@app.route('/register_user', methods=['POST'])
def register_user():
    post_info = request.get_json()
    inst = RegisterUserClass()

    if not check_for_post_params(('username', 'name', 'email', 'password', 'token'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if not is_guest_token_valid(post_info['token']):
        return jsonify({'status': 'error_invalid_guest_token', 'message': 'Guest token is invalid'})

    if check_if_empty(('username', 'name', 'email', 'password'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return inst.run(post_info, get_connection())


@app.route('/login_user', methods=['POST'])
def login_user():
    post_info = request.get_json()
    inst = LoginUserClass()

    if not check_for_post_params(('email', 'password'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('email', 'password'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return inst.login_panel(post_info['email'], post_info['password'], get_connection())


@app.route('/create_problem', methods=['POST'])
def create_problem():
    post_info = request.get_json()

    inst = HandleProblemsClass()

    if not check_for_post_params(('title', 'public', 'text', 'start_date', 'end_date', 'time_limit'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('title', 'public', 'text', 'start_date', 'end_date', 'time_limit'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return inst.create_problem(post_info, get_connection())


@app.route('/')
def debug_page():
    return 'This is the debug page for the backend api. (API works)'


if __name__ == '__main__':
    app.run(port=5100)
