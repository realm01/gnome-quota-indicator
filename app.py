#!/usr/bin/env python3

"""GNOME task bar indicator which shows the user quota of the
currently logged in user"""

from gi.repository import Gtk
from lib.quota_window import QuotaWindow
from lib.quota_indicator import QuotaIndicator
from lib.helpers import load_config


class App(Gtk.Application):
    """Entry point of the indicator app."""

    def __init__(self, name):
        """Ctor Main app."""
        super().__init__()
        self.name = name

        self.config = load_config()

        self.quota_window = QuotaWindow(self)
        self.indicator = QuotaIndicator(self, self.config)

    def run(self):
        """Run app."""
        Gtk.main()


if __name__ == '__main__':
    app = App('Quota Indicator')
    app.run()
