import sqlite3

from flask import request, jsonify
from flask.ext.appbuilder import BaseView, expose, has_access

from domuweb.models import Pin, Event
from domuweb.network import network
from domuweb import automation


class Dashboard(BaseView):
    default_view = "events"
    template_folder = '/home/sebastiano/PycharmProjects/home/fab_addon_lights/fab_addon_lights/templates'

    @expose('/events/')
    @has_access
    def events(self):
        outputs = []
        events = self.appbuilder.get_session.query(Event).filter(Pin.type_id == 0).all()
        for output in self.appbuilder.get_session.query(Pin).filter(Pin.type_id == 1).all():
            output.value = network.get_output(output.code)
            outputs.append(output)
        return self.render_template('list_events.html', events=events, outputs=outputs)

    @expose('/get/', methods=('GET', 'POST'))
    def get(self):
        outputs = []
        for output in self.appbuilder.get_session.query(Pin).filter(Pin.type_id == 1).all():
            outputs.append({'code': output.code, 'value': network.get_output(output.code)})
        return jsonify({"output": outputs})

#TODO: Exec sceneries
    @expose('/set/', methods=('GET', 'POST'))
    def set(self):
        pin_code = request.form['pin_code']
        automation.run(pin_code, 1)
        return self.get()