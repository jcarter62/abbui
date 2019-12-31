from .settings import Settings
import requests, json

class Mrr:

    def __init__(self):
        settings = Settings()
        self.base_url = settings.base_url

    def get_mrr(self):
        results = []
        url = self.base_url + '/mrr'
        try:
            data = requests.get(url)
            results = data.json()['sites']
        except requests.exceptions.RequestException as e:
            print('/mrr exception:' + str(e))
        return results



