"""Controller of Quota Window."""

from lib.mvc.quota_window.model import QuotaWindowModel
from lib.mvc.quota_window.view import QuotaWindowView
from threading import Thread
from lib.helpers import sys_call
from lib.mvc.bases import ControllerBase
from lib.exception_feedback import add_default_exception_handling


class QuotaWindowController(ControllerBase):
    """Controller of Quota Window."""

    def __init__(self, app):
        """Ctor of QuotaWindowController."""
        super().__init__(app, QuotaWindowModel, QuotaWindowView)

        self.usage = None
        self.is_running = False

        self.view.register_on_open(self.on_open)
        self.view.register_on_close(self.on_close)

        self.view.initialize()

    @add_default_exception_handling('Failed to start gathering storate stats')
    def on_open(self):
        """On open event."""
        if not self.is_running:
            self.is_running = True
            self.usage = Usage(
                self.model, self.view.on_update, self.cleanup_thread)
            self.usage.start()

    def on_close(self):
        """On close event."""
        pass

    def cleanup_thread(self):
        """Set is running thread indicator to false."""
        self.is_running = False


class Usage(Thread):
    """Thread which runs du and updates QuotaWindow."""

    def __init__(self, model, on_update, cleanup):
        """Ctor of Usage."""
        super().__init__()
        self.daemon = True
        self.model = model
        self.on_update = on_update
        self.cleanup = cleanup

    @add_default_exception_handling('Failed to get storage usage')
    def run(self):
        """Run du and puts output in an array to display stuff which uses the most quota."""
        out = sys_call('du  --all ~ | sort -n | tail -n 21')
        lines = out.splitlines()
        lines.reverse()
        lines = lines[1:]

        self.model.usage = []
        for line in lines:
            self.model.usage.append({
                'name': ' '.join(line.split()[1:]),
                'size': float(line.split()[0]) / 1024
            })

        self.on_update()
        self.cleanup()
