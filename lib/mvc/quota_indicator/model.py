"""Model classes of Quota Indicator."""

from lib.mvc.bases import ModelBase
from enum import Enum


class MenuItem():
    """Represents a menu item, stores progressbar and label."""

    def __init__(self, progressbar, label):
        """Ctor of MenuItem."""
        self.progressbar = progressbar
        self.label = label


class QuotaState(Enum):
    """Enumerate for the quota state."""
    good = 1
    warning = 2
    critical = 3


class QuotaIndicatorModel(ModelBase):
    """Model of Quota Indicator."""

    def __init__(self):
        """Ctor of QuotaIndicatorModel."""
        super().__init__()
        self.menu_items = {}
        self.quota = {}
        self.fs = []
        self.timers = {
            'warning': 0,
            'critical': 0
        }
