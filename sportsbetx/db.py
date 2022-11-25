"""Connect to the database from the app factory.
this connection is typically tied to the request - it is created at some point when handling a request,
and closed before the response is sent. This is done in init_app()"""
import os,sys

path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, path)

from flask import Flask, current_app, g
from providers.postgre_provider import PostgresDBProvider
from providers.mongo_provider import MongoDBProvider

def get_db(choice):
    if 'db' not in g: # g is a unique global guy
        if choice == 'postgresql':
            provider = PostgresDBProvider()
            provider.read_db_config(filename='dbconfig.ini',section=choice)
        elif(choice == 'mongodb'):
            provider = MongoDBProvider()
                    
        provider.connect()        
        g.db = provider
        # g.db.row_factory = sqlite3.Row # return rows that behave like dicts
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.disconnect()

# def init_db():
#     db = get_db(provider="postgres")

#     with current_app.open_resource('createtables.sql') as f:
#         db.executescript(f.read().decode('utf-8'))
#     print('db initialised')

def init_app(app: "Flask", choice='postgresql'):
    app.teardown_appcontext(close_db)
    with app.app_context(): # needed for the init_db operation and dependency choice
        get_db(choice)

