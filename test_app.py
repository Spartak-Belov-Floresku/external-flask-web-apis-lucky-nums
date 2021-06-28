from unittest import TestCase

from app import app
from helper import UserData

app.config['WTF_CSRF_ENABLED'] = False

class AppTestCase(TestCase):
    """
    runs tests to check data validation, 
    receiving response from the third party server
    """

    def setUp(self):
        
        self.json_data = {'$json':
            {
                'name': 'John',
                'year': 1977,
                'email': 'some@mail.com',
                'color': 'red'
            }
        }

    def test_user_data_validation(self):
        """check if class passes validation"""
        user_data = UserData()

        data, flag = user_data.check_user_data(self.json_data['$json'])

        self.assertEqual(flag, True)

    def test_user_data_invalidation(self):
        """check if class does not passe validation"""
        user_data = UserData()

        self.json_data['$json']['color'] = 'white'

        data, flag = user_data.check_user_data(self.json_data['$json'])

        self.assertEqual(flag, False)
        self.assertEqual(data[1]['color'], 'Invalid value, must be one of: red, green, orange, blue.')


    def test_get_response_from_remote_server(self):
        """check if remote server responded with expected data"""

        user_data = UserData()

        user_data.check_user_data(self.json_data['$json'])

        class_resp = user_data.send_request_to_the_server()

        self.assertEqual(class_resp[0]['status'], True)
        self.assertIn(str(self.json_data['$json']['year']), class_resp[1])


    def test_to_check_responce_app(self):
        """test view of the application"""

        with app.test_client() as c:

            resp = c.post("/api/get-lucky-num", json=self.json_data)

            data = resp.json

            self.assertEqual(resp.status_code, 201)
            self.assertIn(str(self.json_data['$json']['year']), str(data))