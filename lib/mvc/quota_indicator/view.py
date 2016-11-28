"""View of Quota Indicator."""

from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
from lib.helpers import get_path
from lib.mvc.quota_indicator.model import MenuItem


class QuotaIndicatorView():
    """View of Quota Indicator."""

    def __init__(self, app, model):
        """Ctor of QuotaIndicatorView."""
        self.app = app
        self.model = model

        self.upd_quota = None
        self.upd_fs = None

        self.ind = AppIndicator.Indicator.new(
            self.app.name,
            get_path('../img/icon_normal.png'),
            AppIndicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.menu_items = {}
        self.menu = Gtk.Menu()

        self.create_menu_item('quota', self.menu, 'Quota 0/0 MB', self.app.quota_window.view.cb_show)
        for fs in self.model.config['fs']:
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

    def register_update_quota(self, func):
        """Register update quota event."""
        self.upd_quota = func

    def register_update_fs(self, func):
        """Register update fs event."""
        self.upd_fs = func

    def update_quota(self):
        """Update quota event."""
        if self.upd_quota is not None:
            r = self.upd_quota()

            self.menu_items['quota'].label.set_text(r.get('label'))
            self.menu_items['quota'].progressbar.set_fraction(r.get('progress_fraction'))
            self.ind.set_icon(get_path(r.get('icon')))

        return True

    def update_fs(self):
        """Update fs event."""
        if self.upd_fs is not None:
            r = self.upd_fs()

            for ret in r:
                self.menu_items[ret.get('fs')].label.set_text(ret.get('label'))
                self.menu_items[ret.get('fs')].progressbar.set_fraction(ret.get('progress_fraction'))

        return True
