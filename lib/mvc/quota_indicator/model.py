from lib.helpers import load_config

class MenuItem():
    """Represents a menu item, stores progressbar and label."""

    def __init__(self, progressbar, label):
        """Ctor of MenuItem."""
        self.progressbar = progressbar
        self.label = label

class QuotaIndicatorModel():
    def __init__(self):
        self.menu_items = {}
        self.config = load_config()
