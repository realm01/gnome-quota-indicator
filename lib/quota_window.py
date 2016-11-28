"""Quota window package, contains classes for the quota window.

This window shows detailed information about the quota.
"""

from gi.repository import Gtk
from threading import Thread
from time import sleep
from lib.helpers import sys_call, get_path


class QuotaWindow(Gtk.Window):
    """Quota window, which shows a more detailed status about the quota."""

    def __init__(self, app):
        """Quota window ctor."""
        super().__init__()
        self.app = app

        self.connect("delete-event", self.close_window)

        self.set_title(self.app.name)
        self.set_resizable(False)
        self.resize(200, 400)
        self.set_icon_from_file(get_path('../img/icon_normal.png'))

        self.usage = []
        self.usage_updater = Usage(self)
        self.usage_updater.start()

        # create tree view
        self.tree_view = Gtk.TreeView(self.create_model())
        self.tree_view.set_rules_hint(True)

        self.create_columns(self.tree_view)

        # create a grid and attach the treeview to it
        self.grid = Gtk.Grid()
        self.grid.attach(self.tree_view, 0, 0, 1, 1)

        # attach grid to window
        self.add(self.grid)

    def cb_show(self, w, data):
        """On show."""
        self.tree_view.set_model(self.create_model())
        self.show_all()

        return True

    def close_window(self, arg1, arg2):
        self.hide()
        return True

    def create_columns(self, tree_view):
        """Create the columns of the TreeView."""
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("File", rendererText, text=0)
        column.set_sort_column_id(0)
        tree_view.append_column(column)

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Size", rendererText, text=1)
        column.set_sort_column_id(1)
        tree_view.append_column(column)

    def create_model(self):
        """Create model of TreeView which contains the actual data."""
        store = Gtk.ListStore(str, str)

        if(len(self.usage) == 0):
            store.append(['loading', '...'])
            return store

        for file in self.usage:
            store.append([file[1], file[0]])

        return store


class Usage(Thread):
    """Thread which runs du and updates QuotaWindow."""

    def __init__(self, window):
        """Ctor of Usage."""
        super().__init__()
        self.window = window

    def run(self):
        """Run du and puts output in an array to display stuff which uses the most quota."""
        while(True):
            out = sys_call('du  --all ~/.')
            lines = out.splitlines()

            lines.sort(key=lambda x: x[0])
            lines.reverse()
            lines = lines[:20]

            self.window.usage = []
            for line in lines:
                ll = line.split()
                ll[0] = "{0:.4f}".format(float(line[0])/1024) + 'MB'

                self.window.usage.append(ll)

            sleep(10 * 60)
