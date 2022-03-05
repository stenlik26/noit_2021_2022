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
from backend.src.upload_codeplayground.upload_codeplayground import UploadCodePlaygroundClass
from backend.src.upload_codeplayground.load_codeplayground import LoadCodePlayground
from backend.src.admin_panel.admin_panel import AdminPanelClass
from backend.src.handle_user.handle_user import HandleUserClass
from backend.src.upload_picture.upload_picture import PictureUpload

app = Flask(__name__)
flask_cors.CORS(app)


def is_user_valid(token: str, user_id: str) -> bool:
    # TODO: implement this
    return True


def is_guest_token_valid(token: str) -> bool:
    # TODO: implement this
    return True


def is_user_admin_for_group(user_id: str, group_id: str) -> bool:
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

    inst = HandleProblemsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'tests', 'title',
                                  'public', 'text', 'start_date', 'end_date',
                                  'time_limit', 'difficulty', 'groups_to_add_problem'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('user_id', 'token', 'tests', 'title',
                       'public', 'text', 'start_date', 'end_date',
                       'time_limit', 'difficulty'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.create_problem(post_info))


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

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.get_user_group_invites(post_info['user_id']))


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


@app.route('/upload_code', methods=['POST'])
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


@app.route('/get_all_users', methods=['POST'])
def get_all_users():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_all_users(post_info['user_id']))


@app.route('/send_multiple_group_invites', methods=['POST'])
def send_multiple_group_invites():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'invited_ids', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'invited_ids', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.send_multiple_invites(post_info['user_id'], post_info['group_id'], post_info['invited_ids']))


@app.route('/get_groups_user_admin', methods=['POST'])
def get_groups_user_admin():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_groups_where_user_is_admin(post_info['user_id']))


@app.route('/run_problem_tests', methods=['POST'])
def run_problem_tests():
    post_info = request.get_json()

    inst = SolveProblemClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'problem_id', 'code', 'language'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'problem_id', 'code', 'language'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.run_tests(
        post_info['problem_id'],
        post_info['code'],
        post_info['language'],
        post_info['all_tests']))


@app.route('/user_access_to_problem', methods=['POST'])
def user_access_to_problem():
    post_info = request.get_json()

    inst = HandleProblemsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'problem_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'problem_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.does_user_have_access(post_info['user_id'],post_info['problem_id']))


@app.route('/get_all_problems', methods=['POST'])
def get_all_problems():
    post_info = request.get_json()

    inst = HandleProblemsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'difficulty', 'tags', 'name'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'difficulty', 'tags'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_all_problems(post_info['difficulty'], post_info['tags'], post_info['name']))


@app.route('/get_group_access_level', methods=['POST'])
def get_group_access_level():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_user_access_level(post_info['user_id'], post_info['group_id']))


@app.route('/get_group_data', methods=['POST'])
def get_group_data():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_group_info(post_info['group_id'], post_info['user_id']))


@app.route('/get_solutions_to_problem', methods=['POST'])
def get_solutions_to_problem():
    post_info = request.get_json()

    inst = HandleProblemsClass(get_connection())

    if not check_for_post_params(('token', 'my_user_id', 'user_id', 'problem_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'my_user_id', 'user_id', 'problem_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    # По-скоро трябва да се изпълни does_user_have_access

    return jsonify(inst.get_solutions_for_group(post_info['problem_id'],
                                                post_info['user_id'],
                                                post_info['group_problem_ids']))


@app.route('/get_problem_submissions', methods=['POST'])
def get_problem_submissions():
    post_info = request.get_json()

    inst = HandleProblemsClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'solution_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'solution_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_solution_by_id(post_info['solution_id']))


@app.route('/set_comment_to_solution', methods=['POST'])
def set_comment_to_solution():
    post_info = request.get_json()

    inst = SolveProblemClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'solution_id', 'comment'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'solution_id', 'comment'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.comment_solution(post_info['solution_id'], post_info['comment']))


@app.route('/grade_solution', methods=['POST'])
def grade_solution():
    post_info = request.get_json()

    inst = SolveProblemClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'solution_id', 'grade'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'solution_id', 'grade'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.grade_solution(post_info['solution_id'], post_info['grade']))


@app.route('/give_user_admin_access', methods=['POST'])
def give_user_admin_access():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'my_user_id', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'my_user_id', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    # TODO: Check if user is admin
    return jsonify(inst.make_user_admin(post_info['group_id'], post_info['user_id']))


@app.route('/revoke_user_admin_access', methods=['POST'])
def revoke_user_admin_access():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'my_user_id', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'my_user_id', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    # TODO: Check if user is admin
    return jsonify(inst.revoke_user_admin(post_info['group_id'], post_info['user_id']))


@app.route('/kick_user_from_group', methods=['POST'])
def kick_user_from_group():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'my_user_id', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'my_user_id', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    # TODO: Check if user is admin
    return jsonify(inst.remove_user_from_group(post_info['group_id'], post_info['user_id']))


@app.route('/change_group_name', methods=['POST'])
def change_group_name():
    post_info = request.get_json()

    inst = HandleGroupsClass(get_connection())

    if not check_for_post_params(('token', 'my_user_id', 'new_name', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'my_user_id', 'new_name', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    # TODO: Check if user is admin
    return jsonify(inst.change_group_name(post_info['group_id'], post_info['new_name']))


@app.route('/get_time_limit_solution_elapsed', methods=['POST'])
def get_time_limit_solution_elapsed():
    post_info = request.get_json()
    inst = SolveProblemClass(get_connection())

    if not check_for_post_params(('token', 'user_id', 'problem_id', 'time_limit'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'problem_id', 'time_limit'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.init_solution_with_time_limit(post_info))


@app.route('/get_my_groups', methods=['POST'])
def get_my_groups():

    inst = HandleGroupsClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_users_groups(post_info['user_id']))


@app.route('/get_my_solutions', methods=['POST'])
def get_my_solutions():
    inst = HandleProblemsClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_my_solutions(post_info['user_id']))


@app.route('/get_code_info', methods=['POST'])
def get_code_info():
    inst = HandleProblemsClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'code_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'code_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_code_info(post_info['code_id'], post_info['user_id']))


@app.route('/share_solution', methods=['POST'])
def share_solution():
    inst = HandleProblemsClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'code_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'code_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.share_solution(post_info['code_id'], post_info['user_id']))


@app.route('/has_access_to_admin_panel', methods=['POST'])
def has_access_to_admin_panel():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.check_for_access(post_info['user_id']))


@app.route('/get_admin_panel_info', methods=['POST'])
def get_admin_panel_info():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.admin_panel_info())


@app.route('/make_user_admin_on_site', methods=['POST'])
def make_user_admin_on_site():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'to_set_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'to_set_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if inst.check_for_access(post_info['user_id'])['status'] == 'OK':
        return jsonify(inst.make_user_admin(post_info['to_set_user_id']))
    else:
        return jsonify({'status': 'error_no_access', 'message': 'No access to admin panel.'})


@app.route('/revoke_user_admin_on_site', methods=['POST'])
def make_user_admin():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'to_set_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'to_set_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if inst.check_for_access(post_info['user_id'])['status'] == 'OK':
        return jsonify(inst.revoke_user_admin(post_info['to_set_user_id']))
    else:
        return jsonify({'status': 'error_no_access', 'message': 'No access to admin panel.'})


@app.route('/delete_group', methods=['POST'])
def delete_group():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'group_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if inst.check_for_access(post_info['user_id'])['status'] == 'OK':
        return jsonify(inst.delete_group(post_info['group_id']))
    else:
        return jsonify({'status': 'error_no_access', 'message': 'No access to admin panel.'})


@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    inst = HandleUserClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'profile_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'profile_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.get_profile_info(post_info['profile_id']))


@app.route('/change_user_name', methods=['POST'])
def change_user_name():
    inst = HandleUserClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'new_name'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'new_name'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.change_profile_name(post_info['user_id'], post_info['new_name']))


@app.route('/change_user_desc', methods=['POST'])
def change_user_desc():
    inst = HandleUserClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'new_desc'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'new_desc'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    return jsonify(inst.change_description(post_info['user_id'], post_info['new_desc']))


@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    inst = PictureUpload(get_connection())
    post_info = json.loads(request.form['uploadData'])

    if not check_for_post_params(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    file = request.files['uploadedImage']
    return jsonify(inst.upload_picture_for_approval(post_info['user_id'], file))


@app.route('/delete_user', methods=['POST'])
def delete_user():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'to_set_user_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'to_set_user_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if inst.check_for_access(post_info['user_id'])['status'] == 'OK':
        return jsonify(inst.delete_user(post_info['to_set_user_id']))
    else:
        return jsonify({'status': 'error_no_access', 'message': 'No access to admin panel.'})


@app.route('/remove_unapproved_picture', methods=['POST'])
def remove_unapproved_picture():
    inst = AdminPanelClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'picture_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'picture_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if inst.check_for_access(post_info['user_id'])['status'] == 'OK':
        return jsonify(inst.remove_unapproved_picture(post_info['picture_id']))
    else:
        return jsonify({'status': 'error_no_access', 'message': 'No access to admin panel.'})


@app.route('/approve_profile_pic', methods=['POST'])
def approve_profile_pic():
    inst = AdminPanelClass(get_connection())
    inst2 = PictureUpload(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'picture_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'picture_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if inst.check_for_access(post_info['user_id'])['status'] == 'OK':
        return jsonify(inst2.approve_profile_picture(post_info['picture_id']))
    else:
        return jsonify({'status': 'error_no_access', 'message': 'No access to admin panel.'})



@app.route('/upload_codeplayground', methods=['POST'])
def upload_codeplayground():
    inst = UploadCodePlaygroundClass(get_connection())
    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'language', 'code'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'language', 'code'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    return jsonify(inst.upload_code(post_info))


@app.route('/get_codeplayground', methods=['POST'])
def get_codeplayground():
    inst = LoadCodePlayground(get_connection())

    post_info = request.get_json()

    if not check_for_post_params(('token', 'user_id', 'code_id'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if check_if_empty(('token', 'user_id', 'code_id'), post_info):
        return jsonify({'status': 'error_fields_not_filled', 'message': 'Needed fields are empty'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    if not inst.check_if_author(post_info['user_id'], post_info['code_id']):
        return jsonify({'status': 'error_no_access', 'message': 'User doesn\'t have access'})

    return jsonify(inst.get_code_by_object_id(post_info))



@app.route('/', methods=['POST', 'GET'])
def debug_page():
    inst = HandleProblemsClass(get_connection())
    return jsonify(inst.get_code_info('61f44a4d32dc6703d7ff38f3', '616ae290a08c9e9401c2e636'))
    #return jsonify({"test": "api test"})


if __name__ == '__main__':
    app.run(port=5100)
