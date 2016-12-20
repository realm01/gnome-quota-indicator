"""View of QuotaWindowView."""

from gi.repository import Gtk
from lib.mvc.bases import WindowViewBase
from lib.exception_feedback import add_default_exception_handling


class QuotaWindowView(Gtk.Window, WindowViewBase):
    """View of QuotaWindowView."""

    def __init__(self, app, model):
        """Ctor of QuotaWindowView."""
        Gtk.Window.__init__(self)
        ViewBase.__init__(self, app, model)

        self.on_open = None
        self.on_close = None

    @add_default_exception_handling('Failed to initialize Quota Window')
    def initialize(self):
        """Create the actual view with all widgets."""
        self.connect("delete-event", self.cb_close)

        # create tree view
        self.tree_view = Gtk.TreeView(self.model.create_model())

        self.create_columns(self.tree_view)

        # create a grid and attach the treeview to it
        self.grid = Gtk.Grid()
        self.grid.attach(self.tree_view, 0, 0, 1, 1)

        # attach grid to window
        self.add(self.grid)

    @add_default_exception_handling('Failed to open Quota Window')
    def cb_show(self, w, data):
        """On show."""
        self.set_icon_from_file(self.getIcon())

        if self.on_open is not None:
            self.on_open()

        self.tree_view.set_model(self.model.create_model())
        self.show_all()

        return True

    @add_default_exception_handling('Failed to close Quota Window')
    def cb_close(self, w, data):
        """"On window close."""
        if self.on_close is not None:
            self.on_close()

        self.hide()

        return True

    @add_default_exception_handling('Failed to update Quota Window')
    def on_update(self):
        """On update."""
        self.tree_view.set_model(self.model.create_model())

    @add_default_exception_handling()
    def register_on_open(self, func):
        """Register on open event."""
        self.on_open = func

    @add_default_exception_handling()
    def register_on_close(self, func):
        """Register on close event."""
        self.on_close = func

    @add_default_exception_handling('Failed to display storage information')
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
