

class Setup:

    def __init__(self):
        pass

    def clear(self):
        from os import name, getenv, system
        _term = getenv('TERM')
        if getenv('TERM') is None:
            pass
        else:
            if name == 'nt':    # for windows
                _ = system('cls')
            else:   # for mac and linux(here, os.name is 'posix')
                _ = system('clear')

    def user_input(self, msg, def_val) -> str:
        result = def_val
        s = '%s (%s):' % (msg, def_val)
        inp = input(s)
        if inp != '':
            result = inp
        return result

    def execute(self):
        from .settings import Settings
        self.clear()
        settings = Settings()

        settings.base_url = self.user_input(msg='Please provide Base URL', def_val=settings.base_url)

        if self.user_input(msg='Update config file ? ', def_val='yes') == 'yes':
            settings.save_config()

        print(str(settings))
