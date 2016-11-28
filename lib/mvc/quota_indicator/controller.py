"""Controller of Quota Indicator."""

from lib.mvc.quota_indicator.model import QuotaIndicatorModel
from lib.mvc.quota_indicator.view import QuotaIndicatorView
from lib.helpers import sys_call, get_path


class QuotaIndicatorController():
    """Controller of Quota Indicator."""

    def __init__(self, app):
        """Ctor of QuotaIndicatorController."""
        self.model = QuotaIndicatorModel()
        self.view = QuotaIndicatorView(app, self.model)

        self.view.register_update_quota(self.update_quota)
        self.view.register_update_fs(self.update_fs)

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

            if curr / hard >= 0.9:
                ret['icon'] = '../img/icon_warning.png'

            if curr / hard >= 9.9:
                ret['icon'] = '../img/icon_critical.png'

        except:
            ret = {
                'label': 'No Quota',
                'progress_fraction': 0.0,
                'icon': '../img/icon_normal.png'
            }

        return ret

    def update_fs(self):
        """Execute df filter specified fs and update labels."""
        r = []
        for fs in self.model.config['fs']:
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

        return r
