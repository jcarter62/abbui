from data import Settings
import requests


class RemoveToken:

    status: int
    message: str

    def __init__(self, token=''):
        settings = Settings()
        form_data = {'key': settings.key, 'token': token}
        url = settings.base_url + '/removetoken'
        try:
            data = requests.post(url, data=form_data)
            self.status = data.status_code
            if data.status_code == 200:
                self.message = ''
        except Exception as e:
            self.status = 500
            self.message = e.__str__()

        return


