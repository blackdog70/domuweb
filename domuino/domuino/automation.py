import time
import hashlib

from db_session import session, Base
from models import Scenery
from network import network

functions = {}

_inputs = []
_outputs = []


def _get_pin_value(pin):
    device, pin_id = pin.code.split('_')
    if pin.type_id == 0:
        pin_values = _inputs.get(int(device))
    else:
        pin_values = _outputs.get(int(device))
    return pin_values[int(pin_id)] if pin_values else None


def automation(func):
    def wrap(scenery):
        if scenery.start == scenery.end or scenery.start <= time.time() <= scenery.end:
            if scenery.event_value is None or _get_pin_value(scenery.event_pin) == scenery.event_value:
                func(scenery)
    functions[func.__name__] = wrap
    return wrap


@automation
def on(scenery):
    network.pin_on(scenery.output_pin.code)


@automation
def off(scenery):
    network.pin_off(scenery.output_pin.code)


@automation
def forward(scenery):
    print "forward until ref"


@automation
def backward(scenery):
    print "backward until ref"


def run(pin_code = None, value = None):
    global _inputs, _outputs

    _inputs = network.get_inputs()
    _outputs = network.get_outputs()
    if pin_code:
        device, pin_id = pin_code.split('_')
        _inputs[int(device)][int(pin_id)] = int(value)
    for scenery in session.query(Scenery).all():
        functions[scenery.function.name](scenery)


if __name__ == "__main__":
    run()