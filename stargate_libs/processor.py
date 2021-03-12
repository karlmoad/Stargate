from stargate_libs import ConfigurationManager
from stargate_libs import DatabaseConnection
import pandas as pd
import openpyxl
import shortuuid


def get_connection_name(keys):
    return [{'type': 'list',
             'name': 'db',
             "message": 'database connection:',
             'choices': keys
             }]

def get_input_sheet():
    d = {'type': 'input', 'name': 'sheet', 'message': 'worksheet name, defaults to first in workbook:'}
    return d


def get_target_table():
    d = {'type': 'input', 'name': 'table', 'message': 'target database table:'}
    return d


def get_input_file_name():
    d = {'type': 'input', 'name': 'file', 'message': 'input file path:'}
    return d


def get_casing_choice():
    d = {'type': 'list', 'name': 'casing', 'message': 'database type:', 'choices': ['upper', 'lower', 'none'], 'default': 'none'}
    return d


def get_add_uuid_confirmation():
    return [{'type': 'confirm',
             'name': 'uuid',
             'message': 'add a uuid based index column',
             'default': True
             }]


def get_if_exists_choice():
    d = {'type': 'list', 'name': 'if_exists', 'message': 'database type:', 'choices': ['fail', 'append', 'replace'], 'default': 'append'}
    return d


def get_password()
    return {'type': 'password', 'name': 'password', 'message': 'database user password:'}

class Processor:
    def __init__(self, argz, config: ConfigurationManager):
        self._config = config
        self._file = argz.file
        self._table = argz.table
        self._password = argz.password
        self._sheet = argz.sheet
        self._db = argz.db
        self._uuid = argz.uuid
        self._if_exists = argz.if_exists
        self._lower = argz.lower
        self._upper = argz.upper
        self._conn = None
        self._casing = None

        if self._lower != self._upper:
            if self._lower is not None and self._lower:
                self._casing = lambda x: str(x).lower()
            elif self._upper is not None and self._upper:
                self._casing = lambda x: str(x).upper()
        else:
            self._casing = None

    def evaluate_params(self):
        fields = []
        if self._file is None:
            fields.append(get_input_file_name())
        if self._db is None:
            fields.append(get_connection_name(self._config.get_database_connection_names()))
        if self._password is None:
            fields.append(get_password())
        if self._sheet is None:
            fields.append(get_input_sheet())
        if self._table is None:
            fields.append(get_target_table())
        if self._uuid is None:
            fields.append(get_add_uuid_confirmation())
        if self._if_exists is None:
            fields.append(get_if_exists_choice())
        if self._lower is None and self._upper is None:
            fields.append(get_casing_choice())
        return fields

    def load_params(self, params):
        if 'file' in params:
            self._file = params['file']
        if 'password' in params:
            self._password = params['password']
        if 'sheet' in params:
            self._sheet = params['sheet']
        if 'table' in params:
            self._sheet = params['table']
        if 'db' in params:
            self._db = params['db']
        if 'casing' in params:
            choice = params['casing']
            if choice == 'upper':
                self._casing = lambda x: str(x).upper()
            elif choice == 'lower':
                self._casing = lambda x: str(x).lower()
            else:
                self._casing = None
        if 'if_exists' in params:
            self._if_exists = params['if_exists']
        if 'uuid' in params:
            self._uuid = params['uuid'] is True

    def run(self):
        print('_'*80)
        print('Starting process...')
        print('Loading file:{}'.format(self._file))
        sheet = self._sheet
        if len(str(sheet).strip()) <= 0:
            sheet = 0
        data = pd.read_excel(self._file, engine=openpyxl, sheet_name=sheet)
        print('Loaded {} rows.'.format(data.shape[0]))

        if self._casing is not None:
            data.columns = map(self._casing, data.columns)

        if self._uuid:
            data['uuid'] = [shortuuid.uuid() for _ in range(data.shape[0])]

        dbc = DatabaseConnection(self._config)
        r,_ = dbc.initialize(self._db, self._password)
        if not r:
            print('Database configuration: {} does not exist.. terminating'.format(self._db))
            return

        print(dbc.connection_string())

        print(data)