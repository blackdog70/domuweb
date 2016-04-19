import time
import hashlib

from db_session import session, Base
from models import Action
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
    def wrap(action):
        if action.start == action.end or action.start <= time.time() <= action.end:
            if action.event_value is None or _get_pin_value(action.event_pin) == action.event_value:
                func(action)
    functions[func.__name__] = wrap
    return wrap


@automation
def on(action):
    network.pin_on(action.output_pin.code)


@automation
def off(action):
    network.pin_off(action.output_pin.code)


@automation
def forward(action):
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
    for action in session.query(Action).all():
        functions[action.function.name](action)


if __name__ == "__main__":
    run()