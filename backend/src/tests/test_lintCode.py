import flask_unittest

from backend.src.main import app


class LintCodeMainTests(flask_unittest.ClientTestCase):
    app = app

    def test_linter_python(self, client):
        resultFromRequest = client.post('/lint_code', json={

            "code": "\"\"\"\r\nhigh level support for doing this and that.\r\n\"\"\"\nprint(3+3)\n",
            "language": "python",
            "user_id": "test_id",
            "token": "test_token"

        })

        expected_output = {
            "message": {
                "return_code": 0,
                "stderr": "",
                "stdout": "\n--------------------------------------------------------------------\n"
                          "Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)\n\n"
            },
            "status": "OK"
        }

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_linter_wrong_code_python(self, client):
        resultFromRequest = client.post('/lint_code', json={

            "code": "\"\"\"\r\nhigh level support for doing this and that.\r\n\"\"\"\nprint(3+3\n",
            "language": "python",
            "user_id": "test_id",
            "token": "test_token"

        })

        expected_output = {
            "message": {
                "return_code": 2,
                "stderr": "",
                "stdout": "************* Module code\n"
                          "/tmp/test/code.py:5:1: E0001: unexpected EOF "
                          "while parsing (<unknown>, line 5) (syntax-error)\n"
            },
            "status": "OK"
        }

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_token(self, client):
        resultFromRequest = client.post('/lint_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "language": "java",
                "user_id": "test_id"

        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_user_id(self, client):
        resultFromRequest = client.post('/lint_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "language": "java",
                "token": "test_token"

        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_language(self, client):
        resultFromRequest = client.post('/lint_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "user_id": "test_id",
                "token": "test_token"

        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_code(self, client):
        resultFromRequest = client.post('/lint_code', json={
                "language": "java",
                "user_id": "test_id",
                "token": "test_token"
        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)