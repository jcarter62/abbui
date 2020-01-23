from .settings import Settings
import requests, json
import base64

class Sites:

    def __init__(self):
        settings = Settings()
        self.base_url = settings.base_url
        self.sites = []
        self.total_flow = 0.0
        self.mrr_flow = 0.0
        self.get_sites()
        return

    def make_id(self, name):
        bytes_array = str.encode(name)
        encoded = base64.b16encode(bytes_array)
        result = encoded.decode('utf-8')
        return result

    def get_sites(self):
        url = self.base_url + '/api/uihome'
        formdata = {'key': Settings().key}
        try:
            data = requests.post(url, data=formdata)
            if data.status_code != 200:
                return

            jdata = data.json()
            self.sites = jdata['sites']
            self.total_flow = jdata['totalflow']
            self.mrr_flow = jdata['mrrflow']
            #
            # Add row ID
            #
            for s in self.sites:
                s['id'] = self.make_id(s['dispname'])

        except requests.exceptions.RequestException as e:
            print('/api/uihome exception:' + str(e))




