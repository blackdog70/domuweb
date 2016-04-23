from db_session import session
from automation import functions


def init_pin_type():
    session.execute("insert or replace into io_mode values(:id, :name)" ,{"id": 0, "name": "Input"})
    session.execute("insert or replace into io_mode values(:id, :name)" ,{"id": 1, "name": "Output"})
    session.commit()


def init_pin_function():
    session.execute("insert or replace into pin_function values(:id, :type_id, :name)" ,{"id": 0, "type_id": 0, "name": "Button"})
    session.execute("insert or replace into pin_function values(:id, :type_id, :name)" ,{"id": 1, "type_id": 0, "name": "Dimmer"})
    session.execute("insert or replace into pin_function values(:id, :type_id, :name)" ,{"id": 20, "type_id": 1, "name": "Light"})
    session.execute("insert or replace into pin_function values(:id, :type_id, :name)" ,{"id": 21, "type_id": 1, "name": "Light dimmered"})
    session.execute("insert or replace into pin_function values(:id, :type_id, :name)" ,{"id": 22, "type_id": 1, "name": "Socket"})
    session.execute("insert or replace into pin_function values(:id, :type_id, :name)" ,{"id": 23, "type_id": 1, "name": "Balcony"})
    session.commit()


def init_room():
    session.execute("insert or replace into room values(:id, :name)" ,{"id": 100, "name": "Kitchen"})
    session.execute("insert or replace into room values(:id, :name)" ,{"id": 110, "name": "Living"})
    session.execute("insert or replace into room values(:id, :name)" ,{"id": 120, "name": "Bathroom"})
    session.commit()


def fill_function():
    try:
        session.execute("delete from function")
        for function in functions.iterkeys():
            session.execute("insert or replace into function values(:id, :name)", {"id": hash(function),
                                                                                   "name": function})
        session.commit()
    except Exception as e:
        session.rollback()
        print e


fill_function()
init_pin_function()
init_pin_type()
init_room()


session.close()