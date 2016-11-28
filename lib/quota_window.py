"""Quota window package, contains classes for the quota window.

This window shows detailed information about the quota.
"""

from gi.repository import Gtk
import subprocess as sp
from threading import Thread
from time import sleep


class QuotaWindow(Gtk.Window):
    """Quota window, which shows a more detailed status about the quota."""

    def __init__(self, app):
        """Quota window ctor."""
        super().__init__()
        self.app = app
        self.set_title(self.app.name)
        self.set_resizable(False)
        self.resize(200, 400)

        self.usage = []
        self.usage_updater = Usage(self)
        self.usage_updater.start()

    def cb_show(self, w, data):
        """On show."""
        # create tree view
        self.tree_view = Gtk.TreeView(self.create_model())
        self.tree_view.set_rules_hint(True)

        self.create_columns(self.tree_view)

        # create a grid and attach the treeview to it
        grid = Gtk.Grid()
        grid.attach(self.tree_view, 0, 0, 1, 1)

        # attach grid to window
        self.add(grid)
        self.show_all()

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
            store.append(['loading ...', ''])
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
            proc = sp.Popen('du  ~/. | sort -n', stdout=sp.PIPE, shell=True)
            out = proc.communicate()
            out = out[0].decode('utf-8')
            lines = out.splitlines()
            lines.reverse()

            self.window.usage = []
            for line in lines:
                ll = line.split()
                ll[0] = "{0:.4f}".format(float(line[0])/1024) + 'MB'

                self.window.usage.append(ll)

            print(self.window.usage)

            sleep(10 * 60)
