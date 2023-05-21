import psycopg2


class Connector:

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn: psycopg2.connect = None

    def connect(self):
        self.conn = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user,
                                     password=self.password)
