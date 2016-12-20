"""Model of the notification window."""

from lib.mvc.bases import ModelBase

class NotificationWindowModel(ModelBase):
    """Model of the notification window."""

    def __init__(self):
        """Ctor of NotificationWindowModel."""
        super().__init__()
        self.image_path = ''
        self.text = ''
