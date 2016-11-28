#!/usr/bin/env python3

"""GNOME task bar indicator which shows the user quota of the
currently logged in user"""

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
import subprocess as sp


class QuotaIndicator():
    """Indicator Menu."""

    def __init__(self, app):
        """Ctor indicator menu."""
        self.app = app
        self.ind = AppIndicator.Indicator.new(
            self.app.name,
            'Quota',
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()
        item = Gtk.MenuItem()
        box = Gtk.Box(spacing=6)

        # progression bar
        self.quota_progression_bar = Gtk.ProgressBar()
        self.quota_progression_bar.pulse()
        self.quota_progression_bar.show()

        # label
        self.quota_label = Gtk.Label('0/0 MB')

        # add items to box
        box.pack_start(self.quota_progression_bar, True, True, 0)
        box.pack_start(self.quota_label, True, True, 0)

        # add click event to menu item
        item.connect("activate", self.app.quota_window.cb_show, '')
        item.add(box)

        self.menu.append(item)

        # show the menu
        self.menu.show_all()
        self.ind.set_menu(self.menu)

        # refresh quota
        GLib.timeout_add(1000, self.update_quota)

    def cb_exit(self, w, data):
        """On application quit."""
        Gtk.main_quit()

    def update_quota(self):
        """Retrieve quota of current user and update quota label."""
        proc = sp.Popen(['quota'], stdout=sp.PIPE, shell=False)
        out = proc.communicate()
        out = out[0].decode('utf-8')
        lines = out.splitlines()
        quota_a = lines[len(lines) - 1]
        quota_a = quota_a.split()

        curr = float(quota_a[0])
        hard = float(quota_a[2])

        curr = curr / 1024
        hard = hard / 1024

        self.quota_label.set_text(str(int(curr)) + '/' + str(int(hard)) + ' MB')
        self.quota_progression_bar.set_fraction(curr / hard)


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


class App(Gtk.Application):
    """Entry point of the indicator app."""

    def __init__(self, name):
        """Ctor Main app."""
        super().__init__()
        self.name = name
        self.quota_window = QuotaWindow(self)
        self.indicator = QuotaIndicator(self)

    def run(self):
        """Run app."""
        Gtk.main()


if __name__ == '__main__':
    app = App('Quota Indicator')
    app.run()
