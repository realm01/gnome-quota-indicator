"""Functions which are used for displaying exceptions to the user."""


def show_cmd_error(msg, exception):
    """Print a formated error message with reason to the cmd."""
    print('\033[31m{msg}:\033[30m {reason}'.format(msg=msg, reason=str(exception)))
