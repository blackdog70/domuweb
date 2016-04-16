from db_session import session
from automation import functions

def init_pin_type():
    session.execute("insert or replace into input_type values(:id, :name)" ,{"id": 1, "name": "Button"})
    session.execute("insert or replace into input_type values(:id, :name)" ,{"id": 5, "name": "Dimmer"})
    session.execute("insert or replace into output_type values(:id, :name)" ,{"id": 1, "name": "Light"})
    session.execute("insert or replace into output_type values(:id, :name)" ,{"id": 5, "name": "Light dimmered"})
    session.execute("insert or replace into output_type values(:id, :name)" ,{"id": 10, "name": "Socket"})
    session.execute("insert or replace into output_type values(:id, :name)" ,{"id": 20, "name": "Balcony"})


def init_room():
    session.execute("insert or replace into room values(:id, :name)" ,{"id": 100, "name": "Kitchen"})
    session.execute("insert or replace into room values(:id, :name)" ,{"id": 110, "name": "Living"})
    session.execute("insert or replace into room values(:id, :name)" ,{"id": 120, "name": "Bathroom"})

def fill_scenery_type():
    try:
        session.execute("delete from function")
        for function in functions.iterkeys():
            session.execute("insert or replace into function values(:id, :name)", {"id": hash(function),
                                                                                   "name": function})
        session.commit()
    except Exception as e:
        session.rollback()
        print e

fill_scenery_type()
init_pin_type()
init_room()


session.close()