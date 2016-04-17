import os
import time
from threading import Thread, Lock

from communication import Device as Domuino
from db_session import session, Base


class Network(Thread):

    def __init__(self):
        super(Network, self).__init__()
        self.outputs = {}
        self.inputs = {}
        self._devices = {}
        Device = Base.metadata.tables['device']
        for device in session.query(Device).all():
            with Domuino(device.address, device.code, 115200) as d:
                self._devices[device.code] = d

    #TODO: Need To Be Optimized
    def update(self):
        try:
            for device in self._devices.itervalues():
                network_lock.acquire()
                err, outs = device.get_outputs()
                err, ins = device.get_inputs()
                network_lock.release()
                if not err:
                    outputs = outs.split('|')[1]
                    inputs = ins.split('|')[1]
                    if outputs != 'null':
                        self.outputs[device.code] = eval(outputs)
                    if inputs != 'null':
                        self.inputs[device.code] = eval(inputs)
        except Exception as e:
            print e

    @staticmethod
    def _get_pin_value(pins, pin_code):
        network_lock.acquire()
        device, pin_code = pin_code.split('_')
        pin_values = pins.get(int(device))
        network_lock.release()
        return pin_values[int(pin_code)] if pin_values else None

    def get_output(self, pin_code):
        return self._get_pin_value(self.outputs, pin_code)

    def get_input(self, pin_code):
        return self._get_pin_value(self.outputs, pin_code)

    def pin(func):
        def wrap(self, pin_code):
            device, pin = pin_code.split('_')
            device = self._devices.get(int(device))
            if device:
                network_lock.acquire()
                func(self, device, int(pin))
                network_lock.release()
        return wrap

    @pin
    def pin_on(self, device, pin):
        device.on(pin)

    @pin
    def pin_off(self, device, pin):
        device.off(pin)

    def run(self):
        while True:
            self.update()
            time.sleep(0.01)

network_lock = Lock()
network = Network()
if network:
    network.start()

if __name__ == '__main__':
    while True:
        print network.outputs.get(10)
        time.sleep(0.5)
