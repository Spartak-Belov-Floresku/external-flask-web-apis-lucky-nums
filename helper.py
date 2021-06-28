
import random
import requests


"""class will checking, processing and sending user data"""
class UserData:

    def __init__(self):
        self.name = ''
        self.year = 0
        self.email = ''
        self.color = ''

    """method that checks user data for validation and setups flag of result"""
    def check_user_data(self, json):

        colors = ['red', 'green', 'orange', 'blue']

        self.name = json.get('name') or False
        self.year = int(json.get('year') or '0')
        self.email = json.get('email') or False
        self.color = json.get('color')

        err_list = []

        if not self.name:
            err_list.append({'name':'the name is required.'})

        if self.year > 2000 or self.year < 1900:
            err_list.append({'year':'year must be a number between 1900 and 2000'})

        if not self.email:
            err_list.append({'email':'email is required.'})

        if not self.color in colors:
            err_list.append({'color':'Invalid value, must be one of: red, green, orange, blue.'})

        if len(err_list):
            err_list.insert(0,{'status': False})
            return err_list, False

        return [], True

    """
        the method send request to another server and checks result of request.
        If request sussess send data to the user, if not success sends the notification to the users about issues
    """
    def send_request_to_the_server(self):

        rand_number = random.randint(1,100)

        resp1 = requests.get(f'http://numbersapi.com/{self.year}/year?json')
        resp2 = requests.get(f'http://numbersapi.com/{rand_number}?json')
        
        if resp1.status_code == 200 and resp2.status_code == 200:

            return [{'status': True}, resp1.text, resp2.text]

        else:

            return ['server error']

