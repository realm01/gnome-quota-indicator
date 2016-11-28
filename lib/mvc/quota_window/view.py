from gi.repository import Gtk
from lib.helpers import get_path


class QuotaWindowView(Gtk.Window):
    def __init__(self, app, model):
        Gtk.Window.__init__(self)

        self.app = app
        self.model = model

        self.connect("delete-event", self.cb_close)

        self.set_title(self.app.name)
        self.set_resizable(False)
        self.resize(200, 400)
        self.set_icon_from_file(get_path('../img/icon_normal.png'))

        # create tree view
        self.tree_view = Gtk.TreeView(self.model.create_model())
        self.tree_view.set_rules_hint(True)

        self.create_columns(self.tree_view)

        # create a grid and attach the treeview to it
        self.grid = Gtk.Grid()
        self.grid.attach(self.tree_view, 0, 0, 1, 1)

        # attach grid to window
        self.add(self.grid)

    def cb_show(self, w, data):
        """On show."""
        self.tree_view.set_model(self.model.create_model())
        self.show_all()

        return True

    def cb_close(self, w, data):
        """"On window close."""
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
