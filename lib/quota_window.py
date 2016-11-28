"""Quota window package, contains classes for the quota window.

This window shows detailed information about the quota.
"""

from gi.repository import Gtk


class QuotaWindow(Gtk.Window):
    """Quota window, which shows a more detailed status about the quota."""

    def __init__(self, app):
        """Quota window ctor."""
        super().__init__()
        self.app = app
        self.set_title(self.app.name)

    def cb_show(self, w, data):
        """On show."""
        self.show()
