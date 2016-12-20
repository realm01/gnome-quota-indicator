"""Controller of Quota Indicator."""

import sys
from lib.mvc.quota_indicator.model import QuotaIndicatorModel, QuotaState
from lib.mvc.quota_indicator.view import QuotaIndicatorView
from lib.helpers import sys_call, get_path, getuid
from lib.mvc.bases import ControllerBase
from lib.exception_feedback import add_default_exception_handling

from lib.mvc.notification_window.controller import NotificationWindowController

from PIL import Image, ImageDraw, ImageOps

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

        self.notification_window = NotificationWindowController(self.view.app)

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

    def update_notification_window(self):
        show = False
        if self.model.quota['state'] == QuotaState.warning:
            self.notification_window.model.title = 'Your quota is soon full!'
            show = True
        elif self.model.quota['state'] == QuotaState.critical:
            self.notification_window.model.title = 'Your quota is almost full!'
            show = True

        self.notification_window.model.text = 'Current quota usage: ' + str(int(self.model.quota.get('progress_fraction') * 100)) + '%'

        if show:
            self.notification_window.view.cb_show(0, 0)

    @add_default_exception_handling('Failed to generate icon')
    def generateIcon(self, precentage, color):
        icon = Image.open(get_path("../img/icon_default.png"))
        img = Image.new('RGBA', icon.size)

        draw = ImageDraw.Draw(img)

        x = img.size[0]
        y = img.size[1]
        r = x / 4

        x_offset = -1
        y_offset = 7

        draw.pieslice(
            (
                x/2 + x_offset - r,
                y/2 + y_offset - r,
                x/2 + r + x_offset,
                y/2 + r + y_offset
            ),
            -90,
            (360 * precentage) -90,
            fill=color,
            outline=(0, 0, 0))

        del draw

        new_img = Image.alpha_composite(img, icon)
        new_img.save('/tmp/' + getuid() + '_compiled.png', 'PNG')

        icon.close()
        img.close()
        new_img.close()

    @add_default_exception_handling('Failed to gather quota details')
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

            self.model.timers['warning'] -= self.model.config['refresh']['quota_rate']
            self.model.timers['critical'] -= self.model.config['refresh']['quota_rate']

            if curr / hard >= critical_level:
                color = (244, 67, 54)
                if self.model.timers['critical'] <= 0:
                    ret['state'] = QuotaState.critical
            elif curr / hard >= warning_level:
                color = (255, 235, 59)
                if self.model.timers['warning'] <= 0:
                    ret['state'] = QuotaState.warning
            else:
                color = (76, 175, 80)
                ret['state'] = QuotaState.good

            self.generateIcon(curr / hard, color)

            ret['icon'] = '/tmp/' + getuid() + '_compiled.png'

            if self.model.timers['critical'] <= 0:
                self.model.timers['critical'] = self.model.config['refresh']['critical']

            if self.model.timers['warning'] <= 0:
                self.model.timers['warning'] = self.model.config['refresh']['warning']
        except Exception as e:
            print(e)
            ret = {
                'label': 'No Quota',
                'progress_fraction': 0.0,
                'icon': '../img/icon_default.png',
                'state': QuotaState.good
            }

        self.model.quota = ret
        self.update_notification_window()

    @add_default_exception_handling('Failed to gather filesystem details')
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
