from PyInquirer import prompt
from pyfiglet import Figlet
from stargate_libs import ConfigurationManager
from stargate_libs import DatabaseConnection
from tqdm import tqdm
import time


def main_menu():
    return [{'type': 'list',
             'name': 'main',
             'message': 'Main Menu :',
             'choices': ['Configure', 'Import', 'Exit']
             }]

def confirm_menu(msg):
    return [{'type': 'confirm',
             'name': 'confirm',
             'message': msg,
             'default': True
             }]

def config_menu():
    return [{'type': 'list',
             'name': 'config_sub',
             "message": 'Configuration Menu:',
             'choices': ['Database Connections', 'Nuclear Codes', '<Main Menu>']
             }]


def db_conn_menu():
    return [{'type': 'list',
             'name': 'db_config_sub_main',
             "message": 'Database Configuration Menu:',
             'choices': ['New', 'Edit', '<Configuration Menu>']
             }]


def db_conn_edit_menu(keys):
    keys.append('<BACK>')
    return [{'type': 'list',
             'name': 'db_config_sub_edit',
             "message": 'Database Configuration Edit, Select Connection:',
             'choices': keys
             }]

class Interface:
    def __init__(self, argz):
        self._argz = argz
        self._configMar = None
        self._loadConfig()
        self._intro()
        self._main()

    def _loadConfig(self):
        self._configMar = ConfigurationManager()
        if self._argz.config is not None:
            self._configMar.load_alternate(self._argz["config"])

    def _intro(self):
        figlet = Figlet(font='slant')
        print(figlet.renderText("Stargate"))
        print("Transporting your data from excel to databases everywhere\n")
        print("By: Karl Moad")
        print("Certified WORKS ON MY MACHINE approved - 2021")
        print("Provided as is with no expressed warranties of function. You break it, you fix it.")
        print('-'*80)

        # for fun
        # print("Here is a progress bar so you think its doing something important.")
        # foobar = tqdm(total=10)
        # for i in range(10):
        #     foobar.update(1)
        #     time.sleep(.5)
        # foobar.close()
        # end fun

    def _main(self):
        inputz = prompt(main_menu())
        selection = str(inputz['main']).lower()
        if selection == 'configure':
            self._config_menu()
        else:
            return

    def _config_menu(self):
        inputz = prompt(config_menu())
        selection = str(inputz['config_sub']).lower()
        if selection == 'database connections':
            self._database_config_menu()
        else:
            self._main()

    def _database_config_menu(self):
        inputz = prompt(db_conn_menu())
        selection = str(inputz['db_config_sub_main']).lower()
        if selection == 'new':
            self._edit_database_connection()
        elif selection == 'edit':
            keys = self._configMar.get_database_connection_names()
            editz = prompt(db_conn_edit_menu(keys))
            selection_sub = str(editz['db_config_sub_edit'])
            if self._configMar.database_connection_exists(selection_sub):
                self._edit_database_connection(selection_sub)
            else:
                self._database_config_menu()
        else:
            self._config_menu()

    def _edit_database_connection(self, name=None):
        dbc = DatabaseConnection(self._configMar)
        if name is not None:
            dbc.initialize(name)
        props = prompt(dbc.edit())

        savez = prompt(confirm_menu("Save Configuration?"))
        if savez['confirm']:
            dbc.load(props)
            r,m = dbc.save()
            if not r:
                print("Unable to save connection info: reason, {}".format(m))
            else:
                self._configMar.save()
        self._database_config_menu()




