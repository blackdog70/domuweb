from flask import render_template
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from flask.ext.appbuilder import ModelView
from wtforms.validators import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from flask_appbuilder.models.sqla.filters import FilterEqual
from flask_appbuilder.fieldwidgets import Select2Widget

# from models import Room, Device, InputPin, OutputPin, InputType, OutputType, Scenery, Function
from models import Room, Device, Pin, IoMode, PinFunction, Action, Function, Event
from domuweb import appbuilder, db
from network import network

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


# class InputTypeView(ModelView):
#     datamodel = SQLAInterface(InputType)
#
#     base_permissions = ['can_list', 'can_show']
#     show_columns = list_columns = ['name']
#
#
# class OutputTypeView(ModelView):
#     datamodel = SQLAInterface(OutputType)
#
#     base_permissions = ['can_list', 'can_show']
#     show_columns = list_columns = ['name']


class IoModeView(ModelView):
    datamodel = SQLAInterface(IoMode)

    base_permissions = ['can_list', 'can_show']
    show_columns = list_columns = ['name']


class PinFunctionView(ModelView):
    datamodel = SQLAInterface(PinFunction)

    base_permissions = ['can_list', 'can_show']
    show_columns = list_columns = ['name', 'type']


def input_function_query():
    return db.session.query(PinFunction).filter(PinFunction.type_id == 0)


def output_function_query():
    return db.session.query(PinFunction).filter(PinFunction.type_id == 1)


class PinView(ModelView):
    datamodel = SQLAInterface(Pin)

    base_permissions = ['can_list', 'can_show', 'can_edit']
    list_columns = ['name', 'type', 'function', 'device', 'room', ]
    show_columns = list_columns
    edit_columns = ['name', 'function', 'device', 'room', ]


class InputPinView(ModelView):
    datamodel = SQLAInterface(Pin)

    base_permissions = ['can_list', 'can_show', 'can_edit']
    list_columns = ['name', 'type', 'function', 'device', 'room', ]
    show_columns = list_columns
    edit_columns = ['name', 'function', 'device', 'room', ]

    list_title = show_title = edit_title = "Input pins"
    base_filters = [['type_id', FilterEqual, 0]]

    edit_form_extra_fields = {'function':  QuerySelectField('function',
                                                            query_factory=input_function_query,
                                                            widget=Select2Widget(extra_classes=""))}

    def post_update(self, item):
        network.pin_config_input(item.code, item.function.id)


class OutputPinView(ModelView):
    datamodel = SQLAInterface(Pin)

    base_permissions = ['can_list', 'can_show', 'can_edit']
    list_columns = ['name', 'type', 'function', 'device', 'room', ]
    show_columns = list_columns
    edit_columns = ['name', 'function', 'device', 'room', ]

    list_title = show_title = edit_title = "Output pins"
    base_filters = [['type_id', FilterEqual, 1]]

    edit_form_extra_fields = {'function':  QuerySelectField('function',
                                                            query_factory=output_function_query,
                                                            widget=Select2Widget(extra_classes=""))}

    def post_update(self, item):
        network.pin_config_output(item.code, item.function.id)


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


class ActionView(ModelView):
    datamodel = SQLAInterface(Action)

    edit_columns = [
        'parent', 'sequence', 'name', 'ref_pin', 'ref_value', 'function', 'output_pin', 'output_value',
    ]
    add_columns = edit_columns

    list_columns = [
        'sequence', 'name', 'ref_pin', 'ref_value', 'function', 'output_pin', 'output_value',
    ]
    show_columns = list_columns

    add_form_query_rel_fields = {'output_pin': [['type_id', FilterEqual, 1]], }

    list_title = show_title = edit_title = "Actions"


class EventView(ModelView):
    datamodel = SQLAInterface(Event)

    list_columns = [
        'name', 'event_pin', 'event_value', 'start', 'end'
    ]
    add_columns = edit_columns = show_columns = list_columns

    related_views = [ActionView]


db.create_all()

appbuilder.add_view(IoModeView, "Pin types", icon ="fa-envelope", category ="Config")
appbuilder.add_view(PinView, "Pins", icon = "fa-envelope", category = "Config")
appbuilder.add_view(InputPinView, "Input Pins", icon = "fa-envelope", category = "Config")
appbuilder.add_view(OutputPinView, "Output Pins", icon = "fa-envelope", category = "Config")
appbuilder.add_view(PinFunctionView, "Pin Functions", icon = "fa-envelope", category = "Config")
appbuilder.add_view(RoomView, "Rooms", icon = "fa-folder-open-o", category = "Config", category_icon = "fa-envelope")
appbuilder.add_view(DeviceView, "Devices", icon = "fa-envelope", category = "Config")
appbuilder.add_view(FunctionView, "Functions", icon = "fa-envelope", category = "Config")
appbuilder.add_view(EventView, "Events", icon ="fa-envelope", category ="Config")
appbuilder.add_view(ActionView, "Actions", icon ="fa-envelope", category ="Config")
