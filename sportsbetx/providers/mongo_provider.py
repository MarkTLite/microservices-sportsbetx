from datetime import datetime
import os
import mongoengine as db_engine

from db_interface import DatabaseInterface
from dotenv import load_dotenv

class Odds(db_engine.Document):
    """Create a PhoneBook document collection"""
    id = datetime.utcnow()
    contact_name = db_engine.StringField()
    contact_number = db_engine.StringField()

    def to_json(self):
        return {
            "id": self.id,
            "contact_name": self.contact_name,
            "contact_number": self.contact_number
        }

class MongoDBProvider(DatabaseInterface):
    """Implements the [DatabaseInterface] methods to persist data on a mongoDB database."""
    def __init__(self) -> None:
        self.book = None
        self.connect()

    def connect(self):
        try:
            load_dotenv()
            print('Connecting Mongo')
            DB_URI = os.getenv('MONGO_URI')
            db_engine.connect(host=DB_URI)
            print('Mongo Db successfully connected')
            return (True, "Connection Successful")

        except(Exception) as err:
            print(f'Error: {err}')
            return (False, "Error")

    def create(self, location: str, data: dict):        
        try:
            self.book = Odds(
                contact_name = data['contact list'][0][0],
                contact_number = data['contact list'][0][1]
            )
            self.book.save()
            return (True, 'Created')

        except (Exception) as error:
            print(error)
            return (False, "Error")

    def read(self,location: str):
        try:
            if location is None:
                raise Exception()
            data = {'list':[]}
            for contact in Odds.objects:
                data['list'].append(contact.to_json()) 

            return (True, 'Read Successful', data)
        
        except (Exception) as error:
            print(error)
            return (False, "Error", {})

    def update(self, location: str, data: dict):
        try:
            contact_name = data['contact'][1]  # from the test
            contact_number = data['contact'][0]
            self.book = Odds.objects(contact_name=contact_name).first()
            self.book.update(contact_name=contact_name, contact_number=contact_number)
            return (True, 'Update Successful')

        except (Exception) as error:
            print(error)
            return (False, "Error")

    def delete(self,location: str, data: dict):
        try:
            contact_name = data['contact'][0]  # from the test
            self.book = Odds.objects(contact_name=contact_name).first()
            self.book.delete()
            return (True, 'Delete Successful')

        except (Exception) as error:
            print(error)
            return (False, "Error")

    def disconnect(self):
        return (True, "Disconnected")


