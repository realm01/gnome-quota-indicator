#!/usr/bin/env python3

"""GNOME task bar indicator which shows the user quota of the
currently logged in user"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk
from lib.mvc.quota_indicator.controller import QuotaIndicatorController
from lib.mvc.quota_window.controller import QuotaWindowController
import signal


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
    if(os.fork()):
        os._exit(0)

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = App('Quota Indicator')
    app.run()
