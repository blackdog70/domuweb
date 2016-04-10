import os
import time
from threading import Thread, Lock

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
        self._devices = {}
        Device = Base.metadata.tables['device']
        for device in session.query(Device).all():
            with Domuino(device.address, device.code, 115200) as d:
                self._devices[device.code] = d

    #TODO: Need To Be Optimized
    def update(self):
        for device in self._devices.itervalues():
            try:
                network_lock.acquire()
                err, res = device.get_outputs()
                network_lock.release()
                if not err:
                    outputs = res.split('|')[1]
                    if outputs != 'null':
                        self.outputs[device.code] = eval(outputs)
            except Exception as e:
                print e

    def pin_toggle(self, device_code, output_pin):
        device = self._devices.get(int(device_code))
        if device:
            network_lock.acquire()
            device.toggle(output_pin)
            network_lock.release()

    def run(self):
        while True:
            self.update()

network_lock = Lock()
network = Network()
network.start()

if __name__ == '__main__':
    while True:
        print network.outputs.get(10)
        time.sleep(0.5)
