import logging
from flask_appbuilder.basemanager import BaseManager
from flask_babel import lazy_gettext as _
from .views import GroupModelView, ContactModelView

log = logging.getLogger(__name__)

"""
Create your plugin manager, extend from BaseManager.
This will let you create your models and register your views
"""


class ClientAddOnManager(BaseManager):

    def __init__(self, appbuilder):
        """
        Use the constructor to setup any config keys specific for your app.
        """
        super(ClientAddOnManager, self).__init__(appbuilder)
        self.appbuilder.get_app.config.setdefault(
            "CLIENT_ADDON_KEY",
            "d4c1ed1f87507a87df44393a45b545896c757f242eac9cb746469260aa7e4bd7",
        )

    def register_views(self):        
        self.appbuilder.add_view(
            GroupModelView,
            "List Groups",
            icon = "fa-folder-open-o",
            category = "Contacts",
            category_icon = "fa-envelope"
        )
        
        self.appbuilder.add_view(
            ContactModelView,
            "List Contacts",
            icon = "fa-envelope",
            category = "Contacts"
        )

    def pre_process(self):
        pass

    def post_process(self):
        pass
