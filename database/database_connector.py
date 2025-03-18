import sqlite3


class DatabaseConnector:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''
            PRAGMA foreign_keys = ON;
            '''
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.cursor = None
            self.connection = None

    def execute(self, query, params=()):
        if self.cursor:
            self.cursor.execute(query, params)
            self.connection.commit()

    def executemany(self, query, params=()):
        if self.cursor:
            self.cursor.executemany(query, params)
            self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    @property
    def lastrowid(self):
        return self.cursor.lastrowid
