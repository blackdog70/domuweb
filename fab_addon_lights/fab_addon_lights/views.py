import sqlite3

from flask import request, jsonify
from flask.ext.appbuilder import BaseView, expose, has_access

from domuino.models import Pin
from domuino.network import network
from domuino import automation


class Dashboard(BaseView):
    default_view = "sceneries"
    template_folder = '/home/sebastiano/PycharmProjects/home/fab_addon_lights/fab_addon_lights/templates'

    @expose('/sceneries/')
    @has_access
    def sceneries(self):
        outputs = []
        inputs = self.appbuilder.get_session.query(Pin).filter(Pin.type_id == 0).all()
        for output in self.appbuilder.get_session.query(Pin).filter(Pin.type_id == 1).all():
            output.value = network.get_output(output.code)
            outputs.append(output)
        return self.render_template('list_lights.html', inputs=inputs, outputs=outputs)

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