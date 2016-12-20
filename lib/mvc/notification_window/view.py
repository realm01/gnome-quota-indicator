"""View of the notification window."""

from gi.repository import Gtk
from lib.mvc.bases import WindowViewBase
from lib.exception_feedback import add_default_exception_handling


class NotificationWindowView(Gtk.Window, WindowViewBase):
    def __init__(self, app, model):
        """Ctor of NotificationWindowView."""
        Gtk.Window.__init__(self)
        ViewBase.__init__(self, app, model)

    @add_default_exception_handling('Failed to initialize Quota Indicator')
    def initialize(self):
        """Create the actual view with all widgets."""
        self.connect("delete-event", self.cb_close)
