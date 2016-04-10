import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), convert_unicode=True, echo=False)

connection = engine.connect()

def init_pin_type():
    connection.execute('insert or replace into input_type (id, name) values (1, "Button")')
    connection.execute('insert or replace into input_type (id, name) values (5, "Dimmer")')
    connection.execute('insert or replace into output_type (id, name) values (1, "Light")')
    connection.execute('insert or replace into output_type (id, name) values (5, "Light dimmered")')
    connection.execute('insert or replace into output_type (id, name) values (10, "Socket")')
    connection.execute('insert or replace into output_type (id, name) values (20, "Balcony")')

def init_scenery_type():
    connection.execute('insert or replace into scenery_type (id, name) values (100, "On")')
    connection.execute('insert or replace into scenery_type (id, name) values (200, "Off")')
    connection.execute('insert or replace into scenery_type (id, name) values (300, "On until ref")')

init_pin_type()
init_scenery_type()

connection.close()