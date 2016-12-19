"""MVC Base classes."""

from lib.helpers import load_config
from lib.exception_feedback import show_cmd_error


class ModelBase():
    """Base class of all Models."""

    def __init__(self):
        """Ctor of ModelBase, loads config."""
        self.config = load_config()


class ViewBase():
    """Base class of all Views."""

    def __init__(self, app, model):
        """Ctor of ViewBase, stores app and model."""
        self.app = app
        self.model = model


class ControllerBase():
    """Base class of all Controllers."""

    def __init__(self, app, model, view):
        """Ctor of ControllerBase, creates model and view."""
        try:
            self.model = model()
            self.view = view(app, self.model)
        except Exception as e:
            show_cmd_error('Couldnt create model and view', e)
            raise e
