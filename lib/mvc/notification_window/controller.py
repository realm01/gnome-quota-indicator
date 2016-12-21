"""Controller of the notification window."""

from lib.mvc.bases import ControllerBase
from lib.mvc.notification_window.model import NotificationWindowModel
from lib.mvc.notification_window.view import NotificationWindowView
from lib.exception_feedback import add_default_exception_handling

from functools import partial


class NotificationWindowController(ControllerBase):
    """Controller of the notification window."""

    def __init__(self, app):
        """Ctor of NotificationWindowController."""
        super().__init__(app, NotificationWindowModel, NotificationWindowView)
        self.view.register_open_usage_event(
            partial(self.view.app.quota_window.view.cb_show, 0, 0))
        self.view.initialize()
