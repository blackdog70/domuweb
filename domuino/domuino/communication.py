import serial
import time
import json
from random import SystemRandom

from Crypto.Cipher import AES

from PyCRC.CRC16 import CRC16

PASSWORD = "GloriaErikaSeba "
BLOCK_SIZE = 16


class Device(object):

    def __init__(self, port, code, baudrate=9600):
        self.port = port
        self._485 = None
        self.code = code
        self.baudrate = baudrate
        self._crc = CRC16(modbus_flag=True)

    def _set485in(self):
        self._485.setRTS(False)

    def _set485out(self):
        self._485.setRTS(True)

    def _getACK(self):
        try:
            self._set485in()

            data = self._485.readline()[:-2]
            buffer = data[:data.rfind('|')]
            crc = int(data[data.rfind('|') + 1:])
            # IV = self._485.readline()[:-2]
            # buffer_size = int(self._485.readline())
            # crc = int(self._485.readline())
            # buffer = ''
            # for i in xrange(buffer_size):
            #     buffer += self._485.read();
            if self._crc.calculate(buffer) != crc:
                return True, "ERRORE CRC"
            else:
                # aes = AES.new(PASSWORD,AES.MODE_CBC, IV)
                # data = aes.decrypt(buffer).strip()
                # return json.loads(data)
                return False, buffer
        except Exception as e:
            print e

    def _command(self, command):
        if not self._485.is_open:
            self._485.open()
        self._set485out()
        # IV = ''.join([chr(97+SystemRandom().randrange(16)) for rand in xrange(16)])
        # aes = AES.new(PASSWORD, AES.MODE_CBC, IV)
        # span = BLOCK_SIZE-(len(command) % BLOCK_SIZE)
        # text = command + ' ' * span
        # cipher = aes.encrypt(text)
        # self._485.write(str(len(command) + span) + '\n')
        # self._485.write(cipher)
        # self._485.write(IV + '\n')
        # self._485.write(str(self._crc.calculate(cipher)) + '\n')
        data = str(self._crc.calculate(command[:-1])) + '|' + command
        self._485.write(data)
        return self._getACK()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        try:
            self._485 = serial.Serial(self.port, baudrate=self.baudrate, timeout=7)
            # self._485.rs485_mode = serial.rs485.RS485Settings()
            if self._485.is_open:
                self.disconnect()
            self._485.open()
            print self._getACK()
            pass
        except Exception as e:
            print e

    def disconnect(self):
        self._485.close()

    def set(self, out, value):
        pass

    def emon_current(self, pin, value):
        return self._command("EMONC|%s|%s." % (pin, value*100))

    def toggle(self, out):
        return self._command("TOGGLE|%s." % out)

    def on(self, out):
        return self._command("SETP|%s|1." % out)

    def off(self, out):
        return self._command("SETP|%s|0." % out)

    def scenery_on(self, id):
        return self._command("SCON|%s." % id)

    def scenery_off(self, id):
        return self._command("SCOFF|%s." % id)

    def set_value(self, out, value):
        return self._command("SETV|%s|%s." % (out, value))

    def test(self):
        return self._command("TEST.")

    def get_inputs(self):
        return self._command("GETP|I.")

    def get_outputs(self):
        return self._command("GET|O.")

    def get_inputs_value(self):
        return self._command("GETV|I.")

    def get_outputs_value(self):
        return self._command("GETV|O.")

    def get_power(self):
        return self._command("POWER.")

    def set_time(self):
        return self._command("TIME|%s." % int(time.time()))

    def freemem(self):
        return self._command("FREEMEM.")


if __name__ == '__main__':
    def test_commands():
        print d.freemem()
        print d.scenery_on(0)
        print d.scenery_on(1)
        print d.scenery_off(0)
        print d.scenery_off(1)
        print d.set_time()
        print d.get_inputs()
        print d.get_outputs()
        print d.get_inputs_value()
        print d.get_outputs_value()
        print d.on(0)
        print d.on(1)
        print d.off(0)
        print d.toggle(0)
        print d.toggle(0)
        print d.set_value(0, 200)
        print d.freemem()
        print d.get_inputs()
        print d.get_outputs()
        print d.get_inputs_value()
        print d.get_outputs_value()
        print d.off(0)
        print d.off(1)
        print d.emon_current(0, 5)
        print d.freemem()
        print d.emon_current(0, 20.73)
        print d.get_power()

    def test_speed():
        start = time.time()
        msgs = 0
        while True:
            a = d.get_inputs()
            msgs += 1
            if time.time() - start >= 1:
                print a
                print str(msgs)+ "/sec \n"
                msgs = 0
                start = time.time()

    with Device('/dev/ttyUSB0', 1, 115200) as d:
        test_speed()
