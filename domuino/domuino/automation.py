import time
import hashlib

from db_session import session, Base
from models import Scenery
from network import network

functions = {}


def automation(func):
    def wrap(scenery):
        if scenery.start == scenery.end or scenery.start <= time.time() <= scenery.end:
            if scenery.event_value is None or network.get_input(scenery.event_pin.code) == scenery.event_value:
                func(scenery)
        return
    functions[func.__name__] = func
    return wrap


@automation
def toggle(scenery):
    network.pin_toggle(scenery.output_pin)
    print "toggle"


@automation
def forward(scenery):
    print "forward until ref"


@automation
def backward(scenery):
    print "backward until ref"


def run():
    for scenery in session.query(Scenery).all():
        functions[scenery.type](scenery)


if __name__ == "__main__":
    run()