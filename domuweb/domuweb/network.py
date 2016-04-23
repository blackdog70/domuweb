import os
import time
from threading import Thread, Lock

from communication import Device as Domuino
from db_session import session, Base


class Network(Thread):

    def __init__(self):
        super(Network, self).__init__()
        self._outputs = {}
        self._inputs = {}
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
                        self._outputs[device.code] = eval(outputs)
                    if inputs != 'null':
                        self._inputs[device.code] = eval(inputs)
        except Exception as e:
            print e

    @staticmethod
    def _get_pin_value(pins, pin_code):
        device, pin = pin_code.split('_')
        network_lock.acquire()
        pin_values = pins.get(int(device))
        network_lock.release()
        return pin_values[int(pin)] if pin_values else None

    def get_output(self, pin_code):
        return self._get_pin_value(self._outputs, pin_code)

    # def get_input(self, pin_code):
    #     return self._get_pin_value(self._outputs, pin_code)

    def get_inputs(self):
        network_lock.acquire()
        inputs = self._inputs.copy()
        network_lock.release()
        return inputs

    def get_outputs(self):
        network_lock.acquire()
        inputs = self._outputs.copy()
        network_lock.release()
        return inputs

    def pin(func):
        def wrap(self, pin_code, value = None):
            device, pin = pin_code.split('_')
            device = self._devices.get(int(device))
            if device:
                network_lock.acquire()
                if value is None:
                    func(self, device, int(pin))
                else:
                    func(self, device, int(pin), value)
                network_lock.release()
        return wrap

    #TODO: Send config for all ins and outs on network start
    @pin
    def pin_config_input(self, device, pin, value):
        print device.conf_input(pin, value)

    @pin
    def pin_config_output(self, device, pin, value):
        print device.conf_output(pin, value)

    @pin
    def pin_on(self, device, pin):
        print device.on(pin)

    @pin
    def pin_off(self, device, pin):
        print device.off(pin)

    def run(self):
        while True:
            self.update()
            time.sleep(0.01)

network_lock = Lock()
network = None #Network()
if network:
    network.start()

if __name__ == '__main__':
    while True:
        print network._outputs.get(10)
        time.sleep(0.5)
