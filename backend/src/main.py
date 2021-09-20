from flask import Flask, request, jsonify
from backend.src.handle_code.handle_code import HandleCode
import flask_cors
import requests

app = Flask(__name__)
flask_cors.CORS(app)


def is_user_valid(token: str, user_id: str) -> bool:
    # TODO: implement this
    return True


def check_for_post_params(needed_params: tuple, given_params: dict) -> bool:
    return all(key in given_params for key in needed_params)


@app.route('/run_code', methods=['POST'])
def run_code():
    post_info = request.get_json()

    if not check_for_post_params(('user_id', 'code', 'language', 'token'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    if not is_user_valid(post_info['token'], post_info['user_id']):
        return jsonify({'status': 'error_invalid_user', 'message': 'User is invalid'})

    url = 'http://127.0.0.1:5000/run_code'

    inputParams = {
        'language': post_info['language'],
        'code': post_info['code']
    }

    result = requests.post(url=url, json=inputParams)

    data = result.json()

    return data


@app.route('/')
def debug_page():
    return 'This is the debug page for the backend api. (API works)'


if __name__ == '__main__':
    app.run(port=5100)
