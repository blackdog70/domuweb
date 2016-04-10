import os
import time
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from communication import Device as Domuino

basedir = os.path.abspath(os.path.dirname(__file__) + '/..')
engine = create_engine('sqlite:///' + os.path.join(basedir, 'app.db'), convert_unicode=True, echo=False)
Base = declarative_base()
Base.metadata.reflect(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Network(Thread):

    def __init__(self):
        super(Network, self).__init__()
        self.outputs = {}
        self.devices = {}
        Device = Base.metadata.tables['device']
        for device in session.query(Device).all():
            with Domuino(device.address, device.code, 115200) as d:
                self.devices[device.code] = d

    #TODO: Need To Be Optimized
    def update(self):
        for device in self.devices.itervalues():
            try:
                err, res = device.get_outputs()
                if not err:
                    outputs = res.split('@')[0]
                    if outputs != 'null':
                        self.outputs[device.code] = eval(outputs)
            except Exception as e:
                print e

    def run(self):
        while True:
            self.update()


network = Network()
network.start()

if __name__ == '__main__':
    while True:
        print network.outputs.get(10)
        time.sleep(0.5)
