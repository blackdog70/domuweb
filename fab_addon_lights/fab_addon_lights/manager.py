import logging
from flask.ext.appbuilder.basemanager import BaseManager
from .views import Dashboard
from flask_babelpkg import lazy_gettext as _

from domuino.network import network

log = logging.getLogger(__name__)

"""
   Create your plugin manager, extend from BaseManager.
   This will let you create your models and register your views
   
"""


class LightsManager(BaseManager):


    def __init__(self, appbuilder):
        """
             Use the constructor to setup any config keys specific for your app. 
        """
        super(LightsManager, self).__init__(appbuilder)
        self.appbuilder.get_app.config.setdefault('MYADDON_KEY', 'SOME VALUE')

    def register_views(self):
        """
            This method is called by AppBuilder when initializing, use it to add you views
        """
        self.appbuilder.add_view(Dashboard, "lights", category = "Lights")

    def pre_process(self):
        # network.start()
        pass

    def post_process(self):
        pass

