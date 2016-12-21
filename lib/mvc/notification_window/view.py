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

        self.open_usage_event = None

    @add_default_exception_handling('Failed to initialize Quota Indicator')
    def initialize(self):
        """Create the actual view with all widgets."""
        self.connect("delete-event", self.cb_close)

        # change size
        self.resize(200, 150)

        # create vbox
        vbox = Gtk.VBox(spacing=0)

        # create hbox
        hbox = Gtk.HBox(spacing=0)

        # add image to hbox
        self.image = Gtk.Image()
        self.image.set_from_file(self.getIcon())
        hbox.pack_start(self.image, True, True, 0)

        # create vbox_right
        vbox_right = Gtk.VBox(spacing=0)

        # add text to vbox_right
        self.text_label = Gtk.Label(' '.join([self.model.text, self.model.precentage]))
        vbox_right.pack_start(self.text_label, True, True, 0)

        # add vbox_right to hbox
        hbox.pack_start(vbox_right, True, True, 25)

        # add hbox to vbox
        vbox.pack_start(hbox, True, True, 0)

        # create hbox_buttons
        hbox_buttons = Gtk.HBox(spacing=0)

        # add close button to hbox_buttons
        button = Gtk.Button()
        button.set_label("Show Usage")
        button.connect("clicked", self.open_usage, "Show Usage")
        hbox_buttons.pack_start(button, True, True, 0)

        # add close button to hbox_buttons
        button = Gtk.Button()
        button.set_label("Ok")
        button.connect("clicked", self.cb_close, "Ok")
        hbox_buttons.pack_start(button, True, True, 0)

        # add hbox_buttons to vbox
        vbox.pack_start(hbox_buttons, True, True, 0)

        # add vbox to window
        self.add(vbox)

    @add_default_exception_handling()
    def register_open_usage_event(self, func):
        """Register open_usage event."""
        self.open_usage_event = func

    @add_default_exception_handling()
    def open_usage(self, *args):
        """Open usage event."""
        self.open_usage_event()

    @add_default_exception_handling()
    def cb_close(self, w, data):
        """On close event."""
        self.hide()
        return True

    @add_default_exception_handling()
    def cb_show(self, w, data):
        """On show event."""
        self.update()
        self.show_all()

        return True

    @add_default_exception_handling('Failed to update notification window')
    def update(self):
        """Update the notification window view."""
        self.image.set_from_file(self.getIcon())
        self.text_label.set_markup('<span font_weight="bold" foreground="Black" size="large">{text}</span> <span font_weight="bold" color="{color}" background="black" size="large">{precentage}</span>'.format(text=self.model.text, precentage=self.model.precentage, color=self.model.precentage_color))
        self.present()

        return True
