from .app_defaults import Defaults


class Settings:

    def __init__(self, appname='abbui-app'):
        self.appname = appname
        self.base_url = ''
        self.key = ''
        self.load_config()

    def __str__(self):
        nl = '\n'
        s = 'base_url:' + self.base_url + nl + \
            'key:' + self.key + nl + \
            'config file:' + self.config_filename()
        return s

    def config_filename(self):
        import os
        osname = os.name
        if osname == 'nt':
            _data_folder = os.path.join(os.getenv('APPDATA'), self.appname)
        else:
            _data_folder = os.path.join(os.getenv('HOME'), self.appname)

        if not os.path.exists(_data_folder):
            os.makedirs(_data_folder)

        filename = os.path.join(_data_folder, 'settings.json')
        return filename

    def load_config(self):
        import json
        filename = self.config_filename()
        try:
            with open(filename, 'r') as f:
                db_obj = json.load(f)
        except Exception as e:
            # Assume, we do not have a file, create a default object.
            db_obj = {
                "base_url": Defaults().base_url,
                "key": Defaults().key
            }

        try:
            self.base_url = db_obj['base_url']
        except KeyError:
            self.base_url = Defaults().base_url

        try:
            self.key = db_obj['key']
        except KeyError:
            self.key = Defaults().key

        return

    def save_config(self):
        import json
        obj = {
            "base_url": self.base_url,
            "key": self.key
        }

        filename = self.config_filename()
        with open(filename, 'w') as outfile:
            json.dump(obj, outfile)
