from stargate_libs import DatabaseConnection
from tqdm import tqdm

class ImportProcess:
    def __init__(self, argz):
        self._file = argz.file
        self._table = argz.table
        self._password = argz.password
        self._sheet = argz.sheet
        self._db = argz.db
        self._needs=[]

    def evaluate_params(self):
