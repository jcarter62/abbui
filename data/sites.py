from .settings import Settings
import requests, json

class Sites:

    def __init__(self):
        settings = Settings()
        self.base_url = settings.base_url
        self.sites = []
        self.total_flow = 0.0
        self.mrr_flow = 0.0
        self.get_sites()

    def get_sites(self):
        url = self.base_url + '/api/uihome'
        try:
            data = requests.get(url)
            jdata = data.json()
            self.sites = jdata['sites']
            self.total_flow = jdata['totalflow']
            self.mrr_flow = jdata['mrrflow']
        except requests.exceptions.RequestException as e:
            print('/api/uihome exception:' + str(e))




