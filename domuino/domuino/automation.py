import time
import hashlib

from db_session import session, Base
from models import Scenery
from network import network

functions = {}


def automation(func):
    def wrap(scenery):
        print "before"
        if scenery.start == scenery.end or scenery.start <= time.time() <= scenery.end:
            if scenery.event_value is None or network.get_input(scenery.event_pin.code) == scenery.event_value:
                func(scenery)
        print "after"
    functions[func.__name__] = wrap
    return wrap


@automation
def on(scenery):
    network.pin_on(scenery.output_pin.code)
    print "set"


@automation
def off(scenery):
    network.pin_off(scenery.output_pin.code)
    print "res"


@automation
def forward(scenery):
    print "forward until ref"


@automation
def backward(scenery):
    print "backward until ref"


def run():
    for scenery in session.query(Scenery).all():
        functions[scenery.function.name](scenery)


if __name__ == "__main__":
    run()