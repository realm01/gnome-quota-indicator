"""MVC Base classes."""

from lib.helpers import load_config, getuid, get_path
from lib.exception_feedback import show_cmd_error
import os


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


class WindowViewBase(ViewBase):
    """Base class of all windows."""

    def __init__(self, app, model):
        """Ctor of WindowViewBase."""
        super().__init__(app, model)

        self.set_title(self.app.name)
        self.set_resizable(False)
        self.resize(200, 400)
        self.set_icon_from_file(self.getIcon())

    def getIcon(self):
        """Retrieve the path to the icon from /tmp with the UID prepended."""
        failed = False
        try:
            p = '/tmp/' + getuid() + '_compiled.png'
        except Exception as e:
            failed = True

        if not os.path.exists(p) or failed:
            return get_path('../img/icon_default.png')
        else:
            return p

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
