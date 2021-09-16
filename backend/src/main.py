from flask import Flask, request, jsonify
from handle_code.handle_code import HandleCode
import flask_cors
app = Flask(__name__)
flask_cors.CORS(app)


def validate_user(func, post_info):
    # TODO: add user verification here...
    return func


def check_for_post_params(needed_params: tuple, given_params: dict) -> bool:
    if all(key in given_params for key in needed_params):
        return True
    else:
        return False


@app.route('/compile_code', methonds=['POST'])
def compile_code():
    post_info = request.get_json()

    if not check_for_post_params(('user_id', 'code', 'language', 'token'), post_info):
        return jsonify({'status': 'error_missing_params', 'message': 'Needed params are missing'})

    return validate_user(
        HandleCode.execute_code(post_info['code'], post_info['language']),
        post_info
    )
    '''
    Fields:
        - userId
        - code
        - language
        - token
    '''


@app.route('/')
def debug_page():
    return 'This is the debug page for the backend api. (API works)'


if __name__ == '__main__':
    app.run(port="5100")