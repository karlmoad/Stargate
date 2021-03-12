from stargate_libs import ConfigurationManager


def get_database_connection_input_spec(info=None):
    fields = []
    fields.append(get_database_connection_spec_name(info['name'] if 'name' in info else None))
    fields.append(get_database_connection_spec_type(info['type'] if 'type' in info else None))
    fields.append(get_database_connection_spec_host(info['host'] if 'host' in info else None))
    fields.append(get_database_connection_spec_port(info['port'] if 'port' in info else None))
    fields.append(get_database_connection_spec_user(info['user'] if 'user' in info else None))
    fields.append(get_database_connection_spec_schema(info['schema'] if 'schema' in info else None))
    return fields


def eval_database_connection_info(connection_info, include_optional=False):
    fields = []
    if 'type' not in connection_info:
        fields.append(get_database_connection_spec_type())
    if 'host' not in connection_info:
        fields.append(get_database_connection_spec_host())
    if 'port' not in connection_info and include_optional is True:
        fields.append(get_database_connection_spec_port())
    if 'user' not in connection_info:
        fields.append(get_database_connection_spec_user())
    if 'schema' not in connection_info:
        fields.append(get_database_connection_spec_schema())
    if 'password' not in connection_info:
        fields.append(get_database_connection_pwd())
    return fields


def get_database_connection_spec_name(default=None):
    d = {'type': 'input', 'name': 'name', 'message': 'connection name:'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_host(default=None):
    d = {'type': 'input', 'name': 'host', 'message': 'host name or IP:'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_schema(default=None):
    d = {'type': 'input', 'name': 'schema', 'message': 'schema or database name:'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_type(default=None):
    d = {'type': 'list', 'name': 'type', 'message': 'database type:', 'choices': ['mysql', 'sql server']}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_port(default=None):
    d = {'type': 'input', 'name': 'port', 'message': 'host port:'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_spec_user(default=None):
    d = {'type': 'input', 'name': 'user', 'message': 'database user id:'}
    if default is not None:
        d['default'] = default
    return d


def get_database_connection_pwd():
    return {'type': 'password', 'name': 'password', 'message': 'database user password:'}


class DatabaseConnection:
    def __init__(self, configuration_manager: ConfigurationManager):
        self._configMgr = configuration_manager
        self._connInfo = {}
        self._name = None
        self._pwd = None

    def initialize(self, name, password=None):
        exists = False
        need = []
        self._name = name
        if password is not None:
            self._pwd = password

        if self._configMgr.database_connection_exists(name):
            self._connInfo = self._configMgr.get_database_connection(name)
            exists = True

        need = eval_database_connection_info(self._connInfo)
        return exists, need

    def set_properties(self, properties):
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
        if 'schema' in properties:
            self._connInfo['schema'] = properties['schema']

    def save(self):
        return self._save_connection_info()

    def edit(self):
        info = self._serialize()
        if self._pwd is not None:
            info["password"] = self._pwd

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
        if 'schema' in self._connInfo:
            info['schema'] = self._connInfo['schema']

        return info

    def __str__(self):
        return "Name:{}, Type:{}, Host:{}, Port:{}, Schema: {}, User:{}".format(self._name,
                                            self._connInfo['type'] if 'type' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['host'] if 'host' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['port'] if 'port' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['schema'] if 'schema' in self._connInfo else '<UNDEFNINED>',
                                            self._connInfo['user'] if 'user' in self._connInfo else '<UNDEFNINED>')

    def connection_string(self):
        if 'type' not in self._connInfo:
            return ''

        user = self._connInfo['user'] if 'user' in self._connInfo else ''
        pwd = self._pwd if self._pwd is not None else ''
        host = self._connInfo['host'] if 'host' in self._connInfo else ''
        port = ':{}'.format(self._connInfo['port']) if 'port' in self._connInfo and len(str(self._connInfo['port']).strip()) > 0 else ''
        schema = self._connInfo['schema'] if 'schema' in self._connInfo else ''

        # to DBAPI driver specific connection string formatting
        if self._connInfo['type'] == 'mysql':
            return f'mysql+pymysql://{user}:{pwd}@{host}{port}/{schema}?charset=utf8mb4'

        elif self._connInfo['type'] == 'sql server':
            return f'mssql+pyodbc://{user}:{pwd}@{host}{port}/{schema}?driver=SQL+Server+Native+Client+11.0'
        else:
            return ''
