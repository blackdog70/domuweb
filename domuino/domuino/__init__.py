import logging
from flask import Flask
from flask.ext.appbuilder import AppBuilder, SQLA

"""
 Logging configuration
"""


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

# import sys
# sys.path.insert(0, "/var/www/venv/lib/python2.7/pycharm-debug.egg")
# import pydevd
# pydevd.settrace('192.168.1.10', port=39888, stdoutToServer=True, stderrToServer=True)


app = Flask(__name__)
app.config.from_object('config')
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""    

from domuino import views

