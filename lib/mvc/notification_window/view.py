"""View of the notification window."""

from lib.mvc.bases import ViewBase
from lib.exception_feedback import add_default_exception_handling


class NotificationWindowView(ViewBase):
    def __init__(self, app, model):
        """Ctor of NotificationWindowView."""
        super().__init__(app, model)

    @add_default_exception_handling('Failed to initialize Quota Indicator')

    def initialize(self):
        """Create the actual view with all widgets."""
        pass
