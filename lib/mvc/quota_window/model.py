"""Model of Quota Window."""

from gi.repository import Gtk
from lib.mvc.bases import ModelBase


class QuotaWindowModel(ModelBase):
    """Model of Quota Window."""

    def __init__(self):
        """Ctor of QuotaWindowModel."""
        super().__init__()
        self.usage = []

    def create_model(self):
        """Create model of TreeView which contains the actual data."""
        store = Gtk.ListStore(str, float)

        if(len(self.usage) == 0):
            store.append(['loading ...', 0.0])
            return store

        for file in self.usage:
            store.append([file['name'], file['size']])

        return store
