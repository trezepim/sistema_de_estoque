from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, can_write: bool = False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 27017
        self.database_name = "labdatabase"

        try:
            with open("conexion/passphrase/authentication.mongo", "r") as f:
                self.user, self.passwd = f.read().split(',')
        except:
            self.user = None
            self.passwd = None

        self.client = None
        self.db = None

    def connect(self):
        """
        Cria a conexão com o MongoDB utilizando pymongo.
        """
        if self.user:
            uri = f"mongodb://{self.user}:{self.passwd}@{self.host}:{self.port}"
        else:
            uri = f"mongodb://{self.host}:{self.port}"

        self.client = MongoClient(uri)
        self.db = self.client[self.database_name]
        return self.db

    def close(self):
        if self.client:
            self.client.close()

