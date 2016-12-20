"""View of the notification window."""

from gi.repository import Gtk
from lib.mvc.bases import WindowViewBase
from lib.exception_feedback import add_default_exception_handling
from lib.helpers import getuid


class NotificationWindowView(Gtk.Window, WindowViewBase):
    def __init__(self, app, model):
        """Ctor of NotificationWindowView."""
        Gtk.Window.__init__(self)
        WindowViewBase.__init__(self, app, model)

    @add_default_exception_handling('Failed to initialize Quota Indicator')
    def initialize(self):
        """Create the actual view with all widgets."""
        self.connect("delete-event", self.cb_close)

        # create vbox
        vbox = Gtk.VBox(spacing=6)

        # add image to vbox
        self.image = Gtk.Image()
        self.image.set_from_file(self.getIcon())
        vbox.pack_start(self.image, True, True, 0)

        # create hbox
        hbox = Gtk.HBox(spacing=6)

        # add title to hbox
        self.title_label = Gtk.Label(self.model.title)
        hbox.pack_start(self.title_label, True, True, 0)

        # add text to hbox
        self.text_label = Gtk.Label(self.model.text)
        hbox.pack_start(self.text_label, True, True, 0)

        # add hbox to vbox
        vbox.pack_start(hbox, True, True, 0)

        # add vbox to window
        self.add(vbox)

    @add_default_exception_handling()
    def cb_close(self, w, data):
        self.hide()
        return True

    @add_default_exception_handling()
    def cb_show(self, w, data):
        self.update()
        self.show_all()

        return True

    @add_default_exception_handling('Failed to update notification window')
    def update(self):
        self.image.image.set_from_file(self.getIcon())
        self.title_label = Gtk.Label(self.model.title)
        self.text_label = Gtk.Label(self.model.text)

        return True
