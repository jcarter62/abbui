from .settings import Settings
import requests, json

class Sites:

    def __init__(self):
        settings = Settings()
        self.base_url = settings.base_url

    def get_sites(self):
        results = []
        url = self.base_url + '/api/sites'
        try:
            data = requests.get(url)
            results = data.json()['sites']
        except requests.exceptions.RequestException as e:
            print('/api/sites exception:' + str(e))
        return results




