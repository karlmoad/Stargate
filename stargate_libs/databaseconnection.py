from stargate_libs import ConfigurationManager


def get_database_connection_input_spec(info=None):
    fields = []
    fields.append(get_database_connection_spec_name(info['name'] if 'name' in info else None))
    fields.append(get_database_connection_spec_type(info['type'] if 'type' in info else None))
    fields.append(get_database_connection_spec_host(info['host'] if 'host' in info else None))
    fields.append(get_database_connection_spec_port(info['port'] if 'port' in info else None))
    fields.append(get_database_connection_spec_user(info['user'] if 'user' in info else None))
    return fields


def eval_database_connection_info(connection_info):
    fields = []
    if 'type' not in connection_info:
        fields.append(get_database_connection_spec_type())
    if 'host' not in connection_info:
        fields.append(get_database_connection_spec_host())
    if 'port' not in connection_info:
        fields.append(get_database_connection_spec_port())
    if 'user' not in connection_info:
        fields.append(get_database_connection_spec_user())

    fields.append(get_database_connection_pwd())
    return fields


def get_database_connection_spec_name(default=None):
    d = {'type': 'input', 'name': 'name', 'message': 'connection reference name'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_host(default=None):
    d = {'type': 'input', 'name': 'host', 'message': 'host name or IP'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_type(default=None):
    d = {'type': 'list', 'name': 'type', 'message': 'database type', 'choices':['mysql','sql server']}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_port(default=None):
    d = {'type': 'input', 'name': 'port', 'message': 'host port'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_user(default=None):
    d = {'type': 'input', 'name': 'user', 'message': 'user id'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_pwd():
    return {'type': 'password', 'name': 'password', 'message': 'database password'}


class DatabaseConnection:
    def __init__(self, configuration_manager: ConfigurationManager):
        self._configMgr = configuration_manager
        self._connInfo = {}
        self._name = None
        self._pwd = None

    def initialize(self, name):
        out = False
        need = []
        self._name = name
        if self._configMgr.database_connection_exists(name):
            self._connInfo = self._configMgr.get_database_connection(name)

        need = eval_database_connection_info(self._connInfo)
        return out, need

    def load(self, properties):
        if 'name' in properties and self._name is None:
            self._name = properties['name']
        if 'type' in properties:
            self._connInfo['type'] = properties['type']
        if 'host' in properties:
            self._connInfo['host'] = properties['host']
        if 'port' in properties:
            self._connInfo['port'] = properties['port']
        if 'user' in properties:
            self._connInfo['user'] = properties['user']

    def save(self):
        return self._save_connection_info()

    def edit(self):
        info = self._serialize()
        return get_database_connection_input_spec(info)

    def _save_connection_info(self):
        info = self._serialize()
        if self._name is None:
            return False, "Connections can not have a null value name."
        else:
            return self._configMgr.add_database_connection(info)

    def _serialize(self):
        info = {}
        info['name'] = self._name
        if 'type' in self._connInfo:
            info['type'] = self._connInfo['type']
        if 'host' in self._connInfo:
            info['host'] = self._connInfo['host']
        if 'port' in self._connInfo:
            info['port'] = self._connInfo['port']
        if 'user' in self._connInfo:
            info['user'] = self._connInfo['user']
        return info

    def __str__(self):
        return "Name:{}, Type:{}, Host:{},Port:{}, User:{}".format(self._name,
                                            self._connInfo['type'] if 'type' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['host'] if 'host' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['port'] if 'port' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['user'] if 'user' in self._connInfo else '<UNDEFNINED>')


