from .settings import Settings
import requests, json

class Mrr:

    def __init__(self):
        settings = Settings()
        self.base_url = settings.base_url

    def get_mrr(self):
        results = []
        url = self.base_url + '/mrr'
        formdata = {'key': Settings().key}
        try:
            data = requests.post(url, data=formdata)
            if data.status_code != 200:
                return
            results = data.json()['sites']
        except requests.exceptions.RequestException as e:
            print('/mrr exception:' + str(e))
        return results



