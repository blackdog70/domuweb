from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView
from wtforms.validators import ValidationError

from models import Room, Device, InputPin, OutputPin, InputType, OutputType, Scenery, Function
from domuino import appbuilder, db

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


class InputTypeView(ModelView):
    datamodel = SQLAInterface(InputType)

    base_permissions = ['can_list', 'can_show']
    show_columns = list_columns = ['name']


class OutputTypeView(ModelView):
    datamodel = SQLAInterface(OutputType)

    base_permissions = ['can_list', 'can_show']
    show_columns = list_columns = ['name']


class InputPinView(ModelView):
    datamodel = SQLAInterface(InputPin)

    base_permissions = ['can_list', 'can_show', 'can_edit']
    list_columns = ['name', 'type', 'device', 'room', ]
    add_columns = edit_columns = show_columns = list_columns


class OutputPinView(ModelView):
    datamodel = SQLAInterface(OutputPin)

    base_permissions = ['can_list', 'can_show', 'can_edit']
    list_columns = ['name', 'type', 'device', 'room', ]
    add_columns = edit_columns = show_columns = list_columns


class RoomView(ModelView):
    datamodel = SQLAInterface(Room)

    related_views = [InputPinView, OutputPinView]


class DeviceView(ModelView):
    datamodel = SQLAInterface(Device)

    list_columns = ['address', 'code']
    edit_columns = ['address']
    add_columns = show_columns = list_columns

    related_views = [InputPinView, OutputPinView]


class FunctionView(ModelView):
    datamodel = SQLAInterface(Function)

    base_permissions = ['can_list', 'can_show']
    show_columns = list_columns = ['name']


class SceneryView(ModelView):
    datamodel = SQLAInterface(Scenery)

    @staticmethod
    def range0255(self, field):
        if not 0 <= field.data <= 255:
            raise ValidationError('Value must be between 0 and 255')

    list_columns = [
        'name', 'function', 'start', 'end', 'event_pin', 'event_value', 'ref_pin', 'ref_value', 'output_pin', 'output_value',
    ]
    add_columns = edit_columns = show_columns = list_columns
    form_choices = {
        'event_value': [('0', '0'), ('1', '1')],
        'output_value': [('0', '0'), ('1', '1')],
    }
    form_args = {
        'type': {
            'label': 'Automation type',
        },
        'name': {
            'label': 'Scenery Name',
        },
        'start': {
            'label': 'Start time',
#            'widget': widgets.TimePickerWidget()
        },
        'end': {
            'label': 'End time',
#            'widget': widgets.TimePickerWidget()
        },
        'event_value': {
            'label': 'Event value',
        },
        'ref_value': {
            'label': 'Reference value',
            'validators': [range0255]
        },
        'output_value': {
            'label': 'Output value',
        },
    }


db.create_all()

appbuilder.add_view(InputTypeView, "Input Pin types", icon = "fa-envelope", category = "Config")
appbuilder.add_view(OutputTypeView, "Output Pin types", icon = "fa-envelope", category = "Config")
appbuilder.add_view(InputPinView, "Input Pins", icon = "fa-envelope", category = "Config")
appbuilder.add_view(OutputPinView, "Output Pins", icon = "fa-envelope", category = "Config")
appbuilder.add_view(RoomView, "Rooms", icon = "fa-folder-open-o", category = "Config", category_icon = "fa-envelope")
appbuilder.add_view(DeviceView, "Devices", icon = "fa-envelope", category = "Config")
appbuilder.add_view(FunctionView, "Functions", icon = "fa-envelope", category = "Config")
appbuilder.add_view(SceneryView, "Sceneries", icon = "fa-envelope", category = "Config")
