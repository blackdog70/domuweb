from flask.ext.appbuilder import Model
from flask.ext.appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import BigInteger, Column, Integer, String, Float, Boolean, ForeignKey, event
from sqlalchemy.dialects import sqlite
from sqlalchemy.orm import relationship, backref


"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""


class PinType(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name


class PinFunction(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return self.name


class Pin(Model):
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('pin_type.id'), nullable=False)
    type = relationship('PinType', foreign_keys=[type_id])
    function_id = Column(Integer, ForeignKey('pin_function.id'), nullable=False)
    function = relationship('PinFunction', foreign_keys=[function_id])
    device_id = Column(Integer, ForeignKey('device.id'), nullable=False)
    device = relationship('Device', foreign_keys=[device_id]) #, back_populates='device')
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    room = relationship('Room', foreign_keys=[room_id]) #, back_populates='room')

    def __repr__(self):
        return self.name


class Device(Model):
    id = Column(Integer, primary_key=True)
    address = Column(String)
    code = Column(Integer, unique=True)
    input_pins = relationship('Pin',
                              primaryjoin="(Device.id==Pin.device_id) & (Pin.type_id==0)",
                              # foreign_keys=[input_pin_ids],
                              cascade="all, delete-orphan")
    output_pins = relationship('Pin',
                               primaryjoin="(Device.id==Pin.device_id) & (Pin.type_id==1)",
                               # foreign_keys=[output_pin_ids],
                               cascade="all, delete-orphan")

    def __repr__(self):
        return self.address


#TODO: Check if it is in transaction
@event.listens_for(Device, 'after_insert')
def device_after_insert(mapper, connection, target):
    for pin_id in xrange(6):
        pin_code = "%s_%s" % (target.code, pin_id)
        connection.execute('insert into pin (name, code, type_id, function_id, device_id, room_id) '
                           'values("%s - In", "%s", 0, 100, %s, 0)' % (pin_code, pin_code, target.id))
        connection.execute('insert into pin (name, code, type_id, function_id, device_id, room_id) '
                           'values("%s - Out", "%s", 1, 200, %s, 0)' % (pin_code, pin_code, target.id))


class Room(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)

    def __repr__(self):
        return self.name


class Function(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return self.name


class Scenery(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    function_id = Column(Integer, ForeignKey('function.id'), nullable=False)
    function = relationship('Function')
    start = Column(Float)
    end = Column(Float)
    event_pin_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    event_pin = relationship('Pin',
                             # primaryjoin="and_(Pin.id==Scenery.event_pin_id, Pin.type_id==0)",
                             foreign_keys=[event_pin_id])
    event_value = Column(Integer)
    ref_pin_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    ref_pin = relationship('Pin',
                           # primaryjoin="and_(Pin.id==Scenery.ref_pin_id, Pin.type_id==0)",
                           foreign_keys=[ref_pin_id])
    ref_value = Column(Integer)
    output_pin_id = Column(Integer, ForeignKey('pin.id'), nullable=False)
    output_pin = relationship('Pin',
                              # primaryjoin="and_(Pin.id==Scenery.output_pin_id, Pin.type_id==1)",
                              foreign_keys=[output_pin_id])
    output_value = Column(Integer)

    def __repr__(self):
        return self.name


class Datetime(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    datetime = Column(Float)
    value = Column(Integer)

    def __repr__(self):
        return '<datetime %r>' % (self.name)


class ChartConfig(Model):
    id = Column(Integer, primary_key=True)
    period = Column(String)