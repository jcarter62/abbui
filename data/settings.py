class Settings:

    def __init__(self, appname='abbui'):
        self.appname = appname
        self.base_url = ''
        self.load_config()

    def __str__(self):
        nl = '\n'
        s = 'base_url:' + self.base_url + nl + \
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
                "base_url": "http://localhost:5200"
            }

        self.base_url = db_obj['base_url']
        return

    def save_config(self):
        import json
        obj = {
            "base_url": self.base_url
        }

        filename = self.config_filename()
        with open(filename, 'w') as outfile:
            json.dump(obj, outfile)
