import flask_unittest

from backend.src.main import app


class MainTests(flask_unittest.ClientTestCase):
    app = app

    def test_java(self, client):
        resultFromRequest = client.post('/run_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "language": "java",
                "user_id": "test_id",
                "token": "test_token"

        })

        expected_output = {
              "message": {
                "return_code": 0,
                "stderr": "",
                "stdout": "Hello from java\n"
              },
              "status": "OK"
            }

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_csharp(self, client):
        resultFromRequest = client.post('/run_code', json={

            "code": "using System;public class TestProgram{public static void Main(){Console.WriteLine(\"Hello World\");}}",
            "language": "csharp",
            "user_id": "test_id",
            "token": "test_token"

        })

        expected_output = {
              "message": {
                "return_code": 0,
                "stderr": "",
                "stdout": "Hello World\n"
              },
              "status": "OK"
            }

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_python(self, client):
        resultFromRequest = client.post('/run_code', json={

            "code": "print(3+3)\nprint('Hello... testing')",
            "language": "python",
            "user_id": "test_id",
            "token": "test_token"

        })

        expected_output = {
            "message": {
                "return_code": 0,
                "stderr": "",
                "stdout": "6\nHello... testing\n"
            },
            "status": "OK"
        }

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_cpp(self, client):
        resultFromRequest = client.post('/run_code', json={

            "code": "#include <iostream>\nint main(){\nstd::cout<<\"Hello from C++\\n\";\nreturn 0;\n}",
            "language": "cpp",
            "user_id": "test_id",
            "token": "test_token"

        })

        expected_output = {
            "message": {
                "return_code": 0,
                "stderr": "",
                "stdout": "Hello from C++\n"
            },
            "status": "OK"
            }

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_wrong_code_java(self, client):
        resultFromRequest = client.post('/run_code', json={

                "code": "class Simple{pblc static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "language": "java",
                "user_id": "test_id",
                "token": "test_token"

        })

        json_data = resultFromRequest.get_json()
        self.assertEqual(json_data['message']['return_code'], 1)

    def test_wrong_code_csharp(self, client):
        resultFromRequest = client.post('/run_code', json={

            "code": "using System;public class TestProgram{pbic static void Main(){Console.WriteLine(\"Hello World\");}}",
            "language": "csharp",
            "user_id": "test_id",
            "token": "test_token"

        })

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data['message']['return_code'], 1)

    def test_wrong_code_python(self, client):
        resultFromRequest = client.post('/run_code', json={

            "code": "proint(3+3)\nprint('Hello... testing')",
            "language": "python",
            "user_id": "test_id",
            "token": "test_token"

        })

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data['message']['return_code'], 1)

    def test_wrong_code_cpp(self, client):
        resultFromRequest = client.post('/run_code', json={

            "code": "#include <iostream>\nint mion(){\nstd::cout<<\"Hello from C++\\n\";\nreturn 0;\n}",
            "language": "cpp",
            "user_id": "test_id",
            "token": "test_token"

        })

        json_data = resultFromRequest.get_json()
        self.assertEqual(json_data['message']['return_code'], 1)

    def test_missing_token(self, client):
        resultFromRequest = client.post('/run_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "language": "java",
                "user_id": "test_id"

        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_user_id(self, client):
        resultFromRequest = client.post('/run_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "language": "java",
                "token": "test_token"

        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_language(self, client):
        resultFromRequest = client.post('/run_code', json={

                "code": "class Simple{public static void main(String args[]){System.out.println(\"Hello from java\");}}",
                "user_id": "test_id",
                "token": "test_token"

        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)

    def test_missing_code(self, client):
        resultFromRequest = client.post('/run_code', json={
                "language": "java",
                "user_id": "test_id",
                "token": "test_token"
        })

        expected_output = {'status': 'error_missing_params', 'message': 'Needed params are missing'}

        json_data = resultFromRequest.get_json()

        self.assertEqual(json_data, expected_output)
