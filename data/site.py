from .settings import Settings
import requests, json

class Site:

    def __init__(self, sitename = ''):
        settings = Settings()
        self.base_url = settings.base_url
        self.data = {}
        if sitename != '':
            self.get_site(sitename)

    def get_site(self, name=''):
        if name == '':
            return

        url = self.base_url + '/api/uisite/' + name
        formdata = {'key': Settings().key}
        try:
            data = requests.post(url, data=formdata)
            if data.status_code != 200:
                return
            self.data = data.json()
        except requests.exceptions.RequestException as e:
            print('/api/uisite/' + name + ' exception:' + str(e))


