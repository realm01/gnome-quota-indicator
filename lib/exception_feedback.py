"""Functions which are used for displaying exceptions to the user."""

from gi.repository import Gtk
from os import getuid

from threading import Thread

def show_cmd_error(msg, exception):
    """Print a formated error message with reason to the cmd."""
    print('\033[31m{msg}:\033[30m {reason}'.format(msg=msg, reason=str(exception)))


def show_dialog_error(msg, exception):
    """Show an error dialog (Blocking call)."""
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 'Error')
    dialog.format_secondary_text(msg + ': ' + str(exception))
    dialog.run()
    dialog.destroy()

def show_dialog_notification(title, msg):
    """Show a notification dialog (Blocking call)."""
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, title)
    dialog.format_secondary_text(msg)

    image = Gtk.Image()
    image.set_from_file('/tmp/' + str(getuid()) + '_compiled.png')
    dialog.set_image(image)
    dialog.show_all()

    dialog.run()
    dialog.destroy()

def add_default_exception_handling(msg='An error occured'):
    def inner(func):
        def f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                show_dialog_error(msg, e)
        return f
    return inner
