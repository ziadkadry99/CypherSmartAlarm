import sqlite3
from sqlite3 import Error


class DatabaseComs:

    db_connection = None


    db_filename = 'Databases/main.db'


    def __init__(self):
        self.create_db_connectionection()


    def create_db_connectionection(self):
        global db_connection
        try:
            db_connection = sqlite3.connect(self.db_filename)
        except Error as e:
            print(e)


    def close_db_connection(self):
            if db_connection:
                db_connection.close()

    def init_db_tables(self):
        if not db_connection:
            self.create_db_connectionection()
        cursor = self.get_db_cursor()
        if cursor:
            sql_create_encodings_table = """ CREATE TABLE IF NOT EXISTS encodings (
                                                    id integer PRIMARY KEY AUTOINCREMENT,
                                                    name text NOT NULL,
                                                    encoding BLOB NOT NULL,
                                                    image BLOB NOT NULL
                                                ); """
            sql_create_history_table = """ CREATE TABLE IF NOT EXISTS detection_history (
                                                    ticket integer PRIMARY KEY AUTOINCREMENT,
                                                    id text NOT NULL,
                                                    time_date timestamp NOT NULL,
                                                    image BLOB NOT NULL,
                                                    CONSTRAINT face_id
                                                    FOREIGN KEY (id)
                                                    REFERENCES encodings(id)
                                                ); """
            try:
                cursor.execute(sql_create_encodings_table)
                cursor.execute(sql_create_history_table)
            except Error as e:
                print(e)


    def get_db_cursor(self):
        if db_connection:
            return db_connection.cursor()

    def exceute_query(self, query, params = None, retRows = False):
        if not db_connection:
            self.create_db_connectionection()
        cursor = self.get_db_cursor()
        if cursor:
            try:
                if params:
                    cursor.execute(query,params)
                    if retRows:
                        return cursor.fetchall()
                    db_connection.commit()
                else:
                    cursor.execute(query)
                    if retRows:
                        return cursor.fetchall()
                    db_connection.commit()

            except Error as e:
                print(e)
