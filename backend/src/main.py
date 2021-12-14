import datetime
from flask import Flask, request, jsonify
import flask_cors
import requests
from backend.src.mongo_connection.mongo_connection import get_executor_address
from backend.src.mongo_connection.mongo_connection import get_connection
from backend.src.register_user.register_user import RegisterUserClass
from backend.src.login_user.login_user import LoginUserClass
from backend.src.handle_problems.handle_problems import HandleProblemsClass
from backend.src.handle_groups.handle_groups import HandleGroupsClass
from backend.src.solve_problem.solve_problem import SolveProblemClass

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


@app.route('/generate_guest_token', methods=['POST'])
def generate_guest_token():
    post_info = request.get_json()
    inst = LoginUserClass()

    if not check_for_post_params(('timestamp', ), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('timestamp', ), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    token = inst.give_guest_token(post_info['timestamp'])
    return jsonify({'token': token})


@app.route('/validate_token', methods=['POST'])
def validate_token():
    post_info = request.get_json()

    if not check_for_post_params(('token', ), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', ), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(LoginUserClass.validate_token(post_info['token']))


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

    if not data:
        return jsonify({"status": "error", "message": "Internal error, check api and executor."})

    return jsonify(data)


@app.route('/lint_code', methods=['POST'])
def lint_code():
    post_info = request.get_json()

    if not check_for_post_params(('user_id', 'code', 'language', 'token'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    url = get_executor_address() + '/lint'

    inputParams = {
        'language': post_info['language'],
        'code': post_info['code']
    }

    result = requests.post(url=url, json=inputParams)

    data = result.json()

    if not data:
        return jsonify({"status": "error", "message": "Internal error, check api and executor."})

    return jsonify(data)


@app.route('/register_user', methods=['POST'])
def register_user():
    post_info = request.get_json()
    inst = RegisterUserClass()

    if not check_for_post_params(('name', 'email', 'password', 'token'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if not is_guest_token_valid(post_info['token']):
        return jsonify({'status': 'error_invalid_guest_token', 'message': 'Guest token is invalid'})

    if check_if_empty(('name', 'email', 'password'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.run(post_info, get_connection()))


@app.route('/login_user', methods=['POST'])
def login_user():
    post_info = request.get_json()
    inst = LoginUserClass()

    if not check_for_post_params(('email', 'password'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('email', 'password'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.login_panel(post_info['email'], post_info['password'], get_connection()))


@app.route('/create_problem', methods=['POST'])
def create_problem():
    post_info = request.get_json()

    inst = HandleProblemsClass()

    if not check_for_post_params(('token', 'user_id', 'tests', 'title',
                                  'public', 'text', 'start_date', 'end_date', 'time_limit'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('user_id', 'token', 'tests', 'title',
                       'public', 'text', 'start_date', 'end_date', 'time_limit'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.create_problem(post_info, get_connection()))


@app.route('/create_group', methods=['POST'])
def create_group():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'group_name'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('user_id', 'token', 'group_name'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.create_group(post_info))


@app.route('/send_group_invite', methods=['POST'])
def send_group_invite():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'admin_user_id', 'group_id', 'invited_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('admin_user_id', 'token', 'group_id', 'invited_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['admin_user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.send_group_invite(post_info))


@app.route('/reject_group_invite', methods=['POST'])
def reject_group_invite():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'group_id', 'my_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'group_id', 'my_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['my_user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.reject_group_invite(post_info['group_id'], post_info['my_user_id']))


@app.route('/accept_group_invite', methods=['POST'])
def accept_group_invite():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'group_id', 'my_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'group_id', 'my_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['my_user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.accept_group_invite(post_info['group_id'], post_info['my_user_id']))


@app.route('/get_user_group_invites', methods=['POST'])
def get_user_group_invites():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'my_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'my_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['my_user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.get_user_group_invites(post_info['my_user_id']))


@app.route('/get_problem_info', methods=['POST'])
def get_problem_info():
    post_info = request.get_json()

    inst = SolveProblemClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'problem_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'problem_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.get_problem_info(post_info['problem_id']))


@app.route('/upload_code', methods=['POST', 'GET'])
def upload_code():
    post_info = request.get_json()

    inst = SolveProblemClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'problem_id', 'language', 'code'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'problem_id', 'language', 'code'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.upload_solution(post_info))


@app.route('/', methods=['POST', 'GET'])
def debug_page():
    return 'This is the debug page for the backend api. (API works)'


if __name__ == '__main__':
    app.run(port=5100)
