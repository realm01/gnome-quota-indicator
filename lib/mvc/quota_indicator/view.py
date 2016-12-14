"""View of Quota Indicator."""

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
from lib.helpers import get_path
from lib.mvc.quota_indicator.model import MenuItem
from lib.mvc.bases import ViewBase


class QuotaIndicatorView(ViewBase):
    """View of Quota Indicator."""

    def __init__(self, app, model):
        """Ctor of QuotaIndicatorView."""

        super().__init__(app, model)

        self.upd_quota = None
        self.upd_fs = None
        self.quit_event = None
        self.validate_fs = None

        self.ind = AppIndicator.Indicator.new(
            self.app.name,
            get_path('../img/icon_default.png'),
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

    def initialize(self):
        """Create the actual view with all widgets."""
        self.model.menu_items = {}
        self.menu = Gtk.Menu()

        self.create_menu_item('quota', self.menu, ' Quota 0/0 MB | 0%', self.app.quota_window.view.cb_show)
        for fs in self.model.config['fs']:
            self.create_menu_item(fs, self.menu, ' FS 0/0 MB | 0%')

        # quit button
        item = Gtk.MenuItem()
        label = Gtk.Label('Quit')
        label.set_alignment(0.0, 0.0)
        item.connect("activate", self.quit_event, '')
        item.add(label)
        self.menu.append(item)

        # show the menu
        self.menu.show_all()
        self.ind.set_menu(self.menu)

        # refresh quota
        GLib.timeout_add(self.model.config['refresh']['quota_rate'], self.update_quota)

        # refresh fs stats
        GLib.timeout_add(self.model.config['refresh']['fs_rate'], self.update_fs)

        self.update_quota()
        self.update_fs()

    def create_menu_item(self, name, menu, label_text, on_show=None):
        """Create a menu item and appends it to the menu."""
        if name in self.model.menu_items.keys():
            return

        if not name == 'quota' and not self.validate_fs(name):
            return

        item = Gtk.MenuItem()
        grid = Gtk.Grid()

        menu_item = MenuItem(Gtk.ProgressBar(), Gtk.Label(label_text))

        # progression bar
        menu_item.progressbar.pulse()
        menu_item.progressbar.show()

        # add items to grid
        grid.add(menu_item.progressbar)
        grid.attach(menu_item.label, 1, 0, 1, 1)

        # add click event to menu item
        if(on_show is not None):
            item.connect("activate", on_show, '')

        item.add(grid)

        self.model.menu_items[name] = menu_item
        self.menu.append(item)

    def register_update_quota(self, func):
        """Register update quota event."""
        self.upd_quota = func

    def register_update_fs(self, func):
        """Register update fs event."""
        self.upd_fs = func

    def register_quit(self, func):
        """Register quit event."""
        self.quit_event = func

    def register_validate_fs(self, func):
        """Register validate fs event."""
        self.validate_fs = func

    def update_quota(self):
        """Update quota event."""
        if self.upd_quota is not None:
            self.upd_quota()

            self.model.menu_items['quota'].label.set_text(' ' + self.model.quota.get('label') + ' | ' + str(int(self.model.quota.get('progress_fraction') * 100)) + '%')
            self.model.menu_items['quota'].progressbar.set_fraction(self.model.quota.get('progress_fraction'))
            icon_path = self.model.quota.get('icon')
            if icon_path[0] != '/':
                icon_path = get_path(icon_path)

            self.ind.set_icon(icon_path)

        return True

    def update_fs(self):
        """Update fs event."""
        if self.upd_fs is not None:
            self.upd_fs()

            for ret in self.model.fs:
                self.model.menu_items[ret.get('fs')].label.set_text(' ' + ret.get('label') + ' | ' + str(int(ret.get('progress_fraction') * 100)) + '%')
                self.model.menu_items[ret.get('fs')].progressbar.set_fraction(ret.get('progress_fraction'))

        return True
