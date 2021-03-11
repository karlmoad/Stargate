import pathlib
import json


class ConfigurationManager:
    def __init__(self):
        self._defaultDir = "{}/{}".format(str(pathlib.Path.home()), '.stargate')
        self._defaultFile = "{}/{}".format(self._defaultDir, 'config.json')
        self._success = False
        self._config = {}
        self._load()

    def _load(self):
        dir = pathlib.Path(self._defaultDir)
        if not dir.is_dir():
            dir.mkdir(parents=True, exist_ok=True)
            # directory did not exist, so how could the file
            self._success = False
            return

        # we got this far look for the file if so load contents into _config
        cfile = pathlib.Path(self._defaultFile)
        if cfile.exists():
            with cfile.open() as f:
                self._config = json.load(f)
            self._success = True
            return
        else:
            self._success = False
            return

    def is_default_config_loaded(self):
        return self._success

    def load_alternate(self, path):
        file = pathlib.Path(path)
        if file.exists():
            with file.open() as f:
                self._config = json.load(f)
            return True, None
        else:
            return False, "file [{}] does not exist".format(path)

    def save(self):
        file = pathlib.Path(self._defaultFile)
        with file.open("w") as f:
            json.dump(self._config, f)

    def database_connection_exists(self, name):
        if 'connections' not in self._config:
            return False
        if name not in self._config['connections']:
            return False

    def get_database_connection_names(self):
        keys = []
        if 'connections' in self._config:
            keys.extend(self._config['connections'].keys())
        return keys

    def get_database_connection(self, name):
        if 'connections' not in self._config:
            return {}
        if name not in self._config['connections']:
            return {}
        else:
            return self._config['connections'][name]

    def add_database_connection(self, info):
        if 'connections' not in self._config:
            self._config['connections'] = {}

        if 'name' in info:
            self._config['connections'][info['name']] = info
            return True, None
        else:
            return False, "invalid properties"





