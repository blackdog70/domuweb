import sqlite3

from flask import request, jsonify
from flask.ext.appbuilder import BaseView, expose, has_access

from domuino.models import Pin, PinType
from domuino.network import network


class Dashboard(BaseView):
    default_view = "lights"
    template_folder = '/home/sebastiano/PycharmProjects/home/fab_addon_lights/fab_addon_lights/templates'

    def list_lights(self):
        lights = []
        for light in self.appbuilder.get_session.query(Pin).filter(Pin.type_id == 1).all():
            value = None
            outputs = network.outputs.get(light.device.code)
            if outputs:
                value = outputs[light.code]
            lights.append({"name": light.name,
                           "room": str(light.room),
                           "value": value,
                           "code": light.code})
        return lights

    @expose('/lights/')
    @has_access
    def lights(self):
        lights = self.list_lights()
        return self.render_template('list_lights.html', lights=lights)

    @expose('/get/', methods=('GET', 'POST'))
    def get(self):
        lights = self.list_lights()
        return jsonify({"data": lights})

    @expose('/set/', methods=('GET', 'POST'))
    def set(self):
        pin_name = request.form.get('data')
        if pin_name:
            device_code, pin_id = pin_name.split('_')
            network.pin_toggle(device_code, pin_id)
        print request.form.get('data')
        return jsonify(result={})