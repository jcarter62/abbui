from data import Settings
import requests


class TokenOK:
    token: str
    status: str
    message: str

    def __init__(self, token=''):
        self.token = token
        self.status = 'expired'
        self.message = ''
        self.get_token_details()

    def get_token_details(self):
        settings = Settings()
        form_data = {'key': settings.key, 'token': self.token}
        url = settings.base_url + '/token_details'
        try:
            data = requests.post(url, data=form_data)
            if data.status_code == 200:
                self.status = 'OK'
                self.message = ''
                self.token = data.json()['token']
                self.message = ''
        except Exception as e:
            self.message = e.__str__()
