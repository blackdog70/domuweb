import time
import hashlib

from db_session import session, Base
from models import Action, Event
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


def on(action):
    network.pin_on(action.output_pin.code)


def off(action):
    network.pin_off(action.output_pin.code)


def forward(action):
    print "forward until ref"


def backward(action):
    print "backward until ref"


def run(pin_code = None, value = None):
    global _inputs, _outputs

    _inputs = network.get_inputs()
    _outputs = network.get_outputs()
    if pin_code:
        device, pin_id = pin_code.split('_')
        _inputs[int(device)][int(pin_id)] = int(value)

    pin_served = []
    for event in session.query(Event).all():
        if event.start == event.end or event.start <= time.time() <= event.end:
            if _get_pin_value(event.event_pin) == event.event_value:
                for action in event.actions:
                    if action.output_pin not in pin_served:
                        if action.ref_value is None or _get_pin_value(action.ref_pin) == action.ref_value:
                            functions[action.function.name](action)
                            pin_served.append(action.output_pin)

functions['on'] = on
functions['off'] = off
functions['forward'] = forward
functions['backward'] = backward

if __name__ == "__main__":
    run()