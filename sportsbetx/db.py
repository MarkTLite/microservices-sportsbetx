"""Connect to the database from the app factory.
this connection is typically tied to the request - it is created at some point when handling a request,
and closed before the response is sent. This is done in init_app()"""
import sqlite3

from flask import Flask, current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # return rows that behave like dicts

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('createtables.sql') as f:
        db.executescript(f.read().decode('utf-8'))
    print('db initialised')

def init_app(app: "Flask"):
    app.teardown_appcontext(close_db)
    with app.app_context(): # needed for the init_db operation
        init_db()

