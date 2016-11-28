#!/usr/bin/env python3

"""GNOME task bar indicator which shows the user quota of the
currently logged in user"""

from gi.repository import Gtk
from lib.mvc.quota_indicator.controller import QuotaIndicatorController
from lib.mvc.quota_window.controller import QuotaWindowController


class App(Gtk.Application):
    """Entry point of the indicator app."""

    def __init__(self, name):
        """Ctor Main app."""
        super().__init__()
        self.name = name

        self.quota_window = QuotaWindowController(self)
        self.indicator = QuotaIndicatorController(self)

    def run(self):
        """Run app."""
        Gtk.main()


if __name__ == '__main__':
    app = App('Quota Indicator')
    app.run()
