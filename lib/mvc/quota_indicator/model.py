"""Model classes of Quota Indicator."""

from lib.helpers import load_config
from lib.mvc.bases import ModelBase


class MenuItem():
    """Represents a menu item, stores progressbar and label."""

    def __init__(self, progressbar, label):
        """Ctor of MenuItem."""
        self.progressbar = progressbar
        self.label = label


class QuotaIndicatorModel(ModelBase):
    """Model of Quota Indicator."""

    def __init__(self):
        """Ctor of QuotaIndicatorModel."""
        super().__init__()
        self.menu_items = {}
        self.quota = {}
        self.fs = []
