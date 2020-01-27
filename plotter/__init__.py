from data import Settings
import requests, json
from matplotlib import pyplot as plt


class Plotter:

    def __init__(self, site='', days=0.5, filename=''):
        settings = Settings()
        self.base_url = settings.base_url
        self.site = site
        self.days = days
        self.filename = filename
        self.data = {}
        self.get_data()
        self.create_plot_file()

    def get_data(self):
        url = self.base_url + '/api/uisite-plot'
        formdata = {
            'key': Settings().key,
            'site': self.site,
            'days': self.days
        }
        try:
            data = requests.post(url, data=formdata)
            if data.status_code != 200:
                return
            self.data = data.json()
            print(json.dumps(self.data))

        except requests.exceptions.RequestException as e:
            print('/api/uisite-plot exception:' + str(e))
        return

    def create_plot_file(self):
        print('create_plot_file')
        plt.plot(self.data['x'], self.data['y'])
        plt.ylabel('CFS')
        plt.title('Site: %s, flow for %s day(s)' % ( self.site, self.days))
        plt.xticks(self.data['x'], self.data['labels'], rotation='vertical')
        plt.tight_layout()
        plt.grid(which='major', axis='y')
        plt.savefig(self.filename, format='svg')
        plt.close()
        return


