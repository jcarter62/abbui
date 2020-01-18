from data import Settings
import requests
import json


class Login:

    token: str
    message: str

    def __init__(self, username='', password='' ):
        self.message = ''
        if username > '' and password > '':
            self.token = ''
            settings = Settings()
            url = settings.base_url + '/login'
            form_data = {'key': settings.key, 'username': username, 'password': password}
            try:
                data = requests.post(url, data=form_data)
                if data.status_code == 200:
                    self.token = data.json()['token']
                    self.message = ''
            except Exception as e:
                self.message = e.__str__()
        else:
            self.token = ''
            self.message = 'username and/or password blank'
        return

#     def attempt_login(self, username='', password='') -> None:
#         settings = Settings()
#         url = settings.base_url + '/login'
#         form_data = {'key': settings.key, 'username': username, 'password': password}
#         try:
#             data = requests.post(url, data=form_data)
#             if data.status_code != 200:
# #                jdata = data.json()
#                 self.token = data.json()['token']
#                 self.message = ''
#         except Exception as e:
#             self.message = e.__str__()
#
#         return
