"""Functions which are used for displaying exceptions to the user."""

from gi.repository import Gtk


def show_cmd_error(msg, exception):
    """Print a formated error message with reason to the cmd."""
    print('\033[31m{msg}:\033[30m {reason}'.format(
        msg=msg, reason=str(exception)))


def show_dialog_error(msg, exception):
    """Show an error dialog (Blocking call)."""
    dialog = Gtk.MessageDialog(
        None, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 'Error')
    dialog.format_secondary_text(msg + ': ' + str(exception))
    dialog.run()
    dialog.destroy()


def add_default_exception_handling(msg='An error occured'):
    """Decorator generator of default exception handling."""
    def inner(func):
        """Actual decorator for default exception handling."""
        def f(*args, **kwargs):
            """The decorated function for default exception handling."""
            try:
                return func(*args, **kwargs)
            except Exception as e:
                show_dialog_error(msg, e)
        return f
    return inner
