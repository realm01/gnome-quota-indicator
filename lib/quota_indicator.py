"""Quota indicator package, contains classes for the indicator."""

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
from lib.helpers import sys_call, get_path


class MenuItem():
    """Represents a menu item, stores progressbar and label."""

    def __init__(self, progressbar, label):
        """Ctor of MenuItem."""
        self.progressbar = progressbar
        self.label = label


class QuotaIndicator():
    """Indicator Menu."""

    def __init__(self, app, config):
        """Ctor indicator menu."""
        self.app = app
        self.config = config

        self.ind = AppIndicator.Indicator.new(
            self.app.name,
            get_path('../img/icon_normal.png'),
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.menu_items = {}
        self.menu = Gtk.Menu()

        self.create_menu_item('quota', self.menu, 'Quota 0/0 MB', self.app.quota_window.cb_show)
        for fs in self.config['fs']:
            self.create_menu_item(fs, self.menu, 'FS 0/0 MB')

        # show the menu
        self.menu.show_all()
        self.ind.set_menu(self.menu)

        # refresh quota
        GLib.timeout_add(1000, self.update_quota)

        # refresh fs stats
        GLib.timeout_add(1000, self.update_fs)

    def create_menu_item(self, name, menu, label_text, on_show=None):
        """Create a menu item and appends it to the menu."""
        item = Gtk.MenuItem()
        box = Gtk.Box(spacing=6)

        menu_item = MenuItem(Gtk.ProgressBar(), Gtk.Label(label_text))

        # progression bar
        menu_item.progressbar.pulse()
        menu_item.progressbar.show()

        # add items to box
        box.pack_start(menu_item.progressbar, True, True, 0)
        box.pack_start(menu_item.label, True, True, 0)

        # add click event to menu item
        if(on_show is not None):
            item.connect("activate", on_show, '')

        item.add(box)

        self.menu_items[name] = menu_item
        self.menu.append(item)

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

            self.menu_items['quota'].label.set_text('Quota ' + str(int(curr)) + '/' + str(int(hard)) + ' MB')
            self.menu_items['quota'].progressbar.set_fraction(curr / hard)

            if curr / hard >= 0.9:
                self.ind.set_icon(get_path('../img/icon_warning.png'))

            if curr / hard >= 9.9:
                self.ind.set_icon(get_path('../img/icon_critical.png'))

        except:
            self.menu_items['quota'].label.set_text('No Quota')
            self.menu_items['quota'].progressbar.set_fraction(0.0)
            self.ind.set_icon(get_path('../img/icon_normal.png'))

        return True

    def update_fs(self):
        """Execute df filter specified fs and update labels."""
        for fs in self.config['fs']:
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

            self.menu_items[fs].progressbar.set_fraction(used / size)
            self.menu_items[fs].label.set_text(fs + ' ' + used_s + '/' + size_s + size_type)

        return True
