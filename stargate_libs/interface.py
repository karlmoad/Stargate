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
             'choices': ['New', 'Edit', 'View', '<Configuration Menu>']
             }]


def db_conn_select_menu(keys, msg=''):
    keys.append('<BACK>')
    return [{'type': 'list',
             'name': 'db_conn_selection',
             "message": '{}, Select Connection:'.format(msg),
             'choices': keys
             }]


def render(section, func):
    inpt = prompt(func)
    if section in inpt:
        return inpt
    else:
        render(section, func)


class Interface:
    def __init__(self, argz):
        self._argz = argz
        self._configMar = None
        self._loadConfig()
        self._intro()

    def _loadConfig(self):
        self._configMar = ConfigurationManager()
        if self._argz.config is not None:
            self._configMar.load_alternate(self._argz["config"])

    def _intro(self):
        figlet = Figlet(font='slant')
        print(figlet.renderText("Stargate"))
        print("Transporting your data from excel to databases everywhere\n")
        print("By: Karl Moad  (Super Genius)")
        print("Certified WORKS ON MY MACHINE - 2021")
        print("Provided as is with no expressed warranties of function. You break it, you fix it.")
        print('-'*80)



    def start(self):
        # make a decision on if to start interactive session or run process based on arguments
        if self._argz.file is not None:
            self._import()
        else:
            self._main()

    def _main(self):
        inputz = render('main', main_menu())
        if 'main' in inputz:
            selection = str(inputz['main']).lower()
            if selection == 'configure':
               self._config_menu()
            else:
               return
        else:
            return

    def _fun(self):
        code = prompt([{'type': 'input', 'name': 'code', 'message': 'Enter Secret Code:'}])
        confirm = prompt(confirm_menu("Would you like ot play a game?"))
        if 'confirm' in confirm and confirm['confirm']:
            print("Launching the missiles.")
            foobar = tqdm(total=10)
            for i in range(10):
                foobar.update(1)
                time.sleep(.5)
            foobar.close()
            time.sleep(10)
        print("END_OF_LINE")
        return

    def _config_menu(self):
        inputz = render('config_sub', config_menu())
        selection = str(inputz['config_sub']).lower()
        if selection == 'database connections':
            self._database_config_menu()
        elif selection == 'nuclear codes':
            self._fun()
        else:
            self._main()

    def _database_config_menu(self):
        inputz = render('db_config_sub_main', db_conn_menu())
        selection = str(inputz['db_config_sub_main']).lower()
        if selection == 'new':
            self._edit_database_connection()
        elif selection == 'edit' or selection == 'view':
            keys = self._configMar.get_database_connection_names()
            selz = render('db_conn_selection', db_conn_select_menu(keys, msg='{} Database Connection'.format(selection.upper())))
            selection_sub = str(selz['db_conn_selection'])
            if self._configMar.database_connection_exists(selection_sub):
                if selection == 'edit':
                    self._edit_database_connection(selection_sub)
                else:
                    self._view_database_connection(selection_sub)
            else:
                self._database_config_menu()
        else:
            self._config_menu()

    def _view_database_connection(self, name=None):
        dbc = DatabaseConnection(self._configMar)
        dbc.initialize(name)
        print(dbc)
        self._database_config_menu()

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

    def _import(self):
        





