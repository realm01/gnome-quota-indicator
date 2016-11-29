"""Controller of Quota Window."""

from lib.mvc.quota_window.model import QuotaWindowModel
from lib.mvc.quota_window.view import QuotaWindowView
from threading import Thread
from time import sleep
from lib.helpers import sys_call


class QuotaWindowController():
    """Controller of Quota Window."""

    def __init__(self, app):
        """Ctor of QuotaWindowController."""
        self.model = QuotaWindowModel()
        self.view = QuotaWindowView(app, self.model)

        self.usage = Usage(self.model)
        self.usage.start()


class Usage(Thread):
    """Thread which runs du and updates QuotaWindow."""

    def __init__(self, model):
        """Ctor of Usage."""
        super().__init__()
        self.model = model

    def run(self):
        """Run du and puts output in an array to display stuff which uses the most quota."""
        while(True):
            out = sys_call('du  --all ~/. | sort -n | tail -n 21')
            lines = out.splitlines()
            lines.reverse()
            lines = lines[1:]

            self.model.usage = []
            for line in lines:
                ll = line.split()
                ll[0] = "{0:.4f}".format(float(ll[0])/1024) + 'MB'

                self.model.usage.append(ll)

            sleep(10 * 60)
