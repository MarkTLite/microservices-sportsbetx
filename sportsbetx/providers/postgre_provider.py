
from db_interface import DatabaseInterface
from configparser import ConfigParser
import psycopg2, os

class PostgresDBProvider(DatabaseInterface):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def read_db_config(self, filename='dbconfig.ini',section='postgresql'):
        parser = ConfigParser()
        path = os.path.dirname(os.path.abspath(__file__))
        parser.read(path + f'\{filename}')
        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def connect(self):
        """ Connect to the PostgreSQL database server """
        self.conn = None
        try:
            params = self.read_db_config()
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor()
            print('PostgreSQL database version:')
            self.cursor.execute('SELECT version()')
            db_version = self.cursor.fetchone()
            print(db_version)
            return (True, 'Connection Successful')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

    def disconnect(self):
        if self.conn:
            self.conn.close()

        return (True, "Disconnected")

    def create(self, location: str, data: dict):
        """Create a table if it doesnot exists, insert the contact"""
        sql_command = """CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                contact_name VARCHAR(100) NOT NULL,
                contact_number VARCHAR(100) NOT NULL
            );
        """
        try:
            params = self.read_db_config()
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql_command)            
            self.conn.commit()
            if data: 
               self.insert(data=data)
            else:
                raise Exception()

            self.cursor.close()
            self.conn.close()            
            return (True, 'Created')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")
        
        finally:
            if self.conn:
                self.conn.close()

    def read(self, location: str):
        """Read by contact id"""
        sql = "SELECT * FROM phonebook"
        self.conn = None
        try:
            if location is None:
                raise Exception()
            params = self.read_db_config()
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            data = {'list':[]}
            for row in rows:
                data['list'].append(row)                

            self.cursor.close()
            return (True, 'Read Successful', data)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error", {})

        finally:
            if self.conn:
                self.conn.close()

    def insert(self, data: dict):
        """ insert multiple rows into the table  """
        sql = "INSERT INTO phonebook(contact_name , contact_number) VALUES(%s,%s)"
        self.conn = None
        try:
            params = self.read_db_config()
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor()
            if data:
               self.cursor.executemany(sql,data['contact list'])
               self.conn.commit()
               return (True, 'Insert Successful')
            else:
                raise Exception()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

    def update(self, location: str, data: dict):
        """ update contact number based on the name"""
        sql = """UPDATE phonebook
                    SET contact_number = %s
                    WHERE contact_name = %s"""
        self.conn = None
        try:
            if data is None:
                raise Exception()
            params = self.read_db_config()
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql, data['contact'])
            updated_rows = self.cursor.rowcount
            self.conn.commit()
            self.cursor.close()
            return (True, 'Update Successful')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

        finally:
            if self.conn:
                self.conn.close()

    def delete(self, location: str, data: dict):
        """ delete row by data given"""
        try:
            params = self.read_db_config()
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor()
            value= data['contact'][0]
            print(value)
            self.cursor.execute("DELETE FROM phonebook WHERE contact_name = %s", (value,))
            # rows_deleted = self.cursor.rowcount
            self.conn.commit()
            self.cursor.close()
            return (True, 'Delete Successful')

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return (False, "Error")

        finally:
            if self.conn:
                self.conn.close()
