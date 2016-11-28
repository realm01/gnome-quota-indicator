from gi.repository import Gtk


class QuotaWindowModel():
    def __init__(self):
        self.usage = []

    def create_model(self):
        """Create model of TreeView which contains the actual data."""
        store = Gtk.ListStore(str, str)

        if(len(self.usage) == 0):
            store.append(['loading', '...'])
            return store

        for file in self.usage:
            store.append([file[1], file[0]])

        return store
