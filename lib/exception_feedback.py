"""Functions which are used for displaying exceptions to the user."""

from gi.repository import Gtk


def show_cmd_error(msg, exception):
    """Print a formated error message with reason to the cmd."""
    print('\033[31m{msg}:\033[30m {reason}'.format(msg=msg, reason=str(exception)))

def show_dialog_error(app, msg, exception):
    """Show an error dialog (Blocking call)."""
    dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 'Error')
    dialog.format_secondary_text(msg + ': ' + str(exception))
    dialog.run()
    dialog.destroy()
