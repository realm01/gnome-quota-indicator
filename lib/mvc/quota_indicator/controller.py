"""Controller of Quota Indicator."""

import sys
from lib.mvc.quota_indicator.model import QuotaIndicatorModel
from lib.mvc.quota_indicator.view import QuotaIndicatorView
from lib.helpers import sys_call, get_path
from lib.mvc.bases import ControllerBase


class QuotaIndicatorController(ControllerBase):
    """Controller of Quota Indicator."""

    def __init__(self, app):
        """Ctor of QuotaIndicatorController."""
        super().__init__(app, QuotaIndicatorModel, QuotaIndicatorView)

        self.quit_event = None

        self.view.register_update_quota(self.update_quota)
        self.view.register_update_fs(self.update_fs)
        self.view.register_quit(self.quit)
        self.view.register_validate_fs(self.validate_fs)

        self.view.initialize()

    def register_quit(self, func):
        """Register quit event."""
        self.quit_event = func

    def quit(self, *args):
        """Quit event."""
        self.quit_event()

    def validate_fs(self, name):
        """Check if a given path is in df."""
        out = sys_call('df -h | grep ' + name)
        return not out.strip() == ''

    def update_quota(self):
        """Retrieve quota of current user and update quota label."""
        out = sys_call('quota')

        try:
            lines = out.splitlines()
            quota_a = lines[len(lines) - 1]
            quota_a = quota_a.split()

            curr = float(quota_a[0])
            hard = float(quota_a[2])

            curr = curr / 1024
            hard = hard / 1024

            ret = {
                'label': 'Quota ' + str(int(curr)) + '/' + str(int(hard)) + ' MB',
                'progress_fraction': curr / hard
            }

            warning_level = self.model.config.get('notify_levels')
            if warning_level is not None:
                warning_level = warning_level.get('warning')

            if warning_level is None:
                warning_level = 0.8

            critical_level = self.model.config.get('notify_levels')
            if critical_level is not None:
                critical_level = critical_level.get('critical')

            if critical_level is None:
                critical_level = 0.9

            if curr / hard >= critical_level:
                ret['icon'] = '../img/icon_critical.png'
            elif curr / hard >= warning_level:
                ret['icon'] = '../img/icon_warning.png'
            else:
                ret['icon'] = '../img/icon_normal.png'

        except:
            ret = {
                'label': 'No Quota',
                'progress_fraction': 0.0,
                'icon': '../img/icon_normal.png'
            }

        self.model.quota = ret

    def update_fs(self):
        """Execute df filter specified fs and update labels."""
        r = []
        for fs in self.model.menu_items.keys():
            out = sys_call('df | grep ' + fs)
            ll = out.split()

            if(len(ll) < 3):
                continue

            size = float(ll[1])
            used = float(ll[2])

            divisor = 1024
            formator = "{0:.2f}"
            size_type = ' MB'
            if size / 1024 > 10000:
                divisor *= 1024
                size_type = ' GB'

            size_s = formator.format(size / divisor)
            used_s = formator.format(used / divisor)

            r.append({
                'fs': fs,
                'label': fs + ' ' + used_s + '/' + size_s + size_type,
                'progress_fraction': used / size
            })

        self.model.fs = r
