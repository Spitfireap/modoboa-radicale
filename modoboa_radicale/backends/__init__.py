"""Calendar backend definition."""

from importlib import import_module

from modoboa.lib.cryptutils import decrypt


class CalendarBackend(object):
    """Base backend class."""

    def __init__(self, calendar):
        """Default constructor."""
        self.calendar = calendar

    def create_event(self, event):
        """Create a new event."""
        raise NotImplementedError

    def get_event(self, uid):
        """Retrieve an even using its uid."""
        raise NotImplementedError

    def get_events(self, start, end):
        """Retrieve a list of event."""
        raise NotImplementedError

    def delete_event(self, uid):
        """Delete an event using its uid."""
        raise NotImplementedError


def get_backend(name, *args, **kwargs):
    """Return a backend instance."""
    module = import_module("modoboa_radicale.backends.{}".format(name))
    return getattr(
        module, "{}Backend".format(name.capitalize()))(*args, **kwargs)


def get_backend_from_request(name, request, *args, **kwargs):
    """Return a backend instance from a request."""
    calendar = request.user.mailbox.usercalendar_set.first()
    password = decrypt(request.session["password"])
    return get_backend(
        name, calendar, request.user.email, password)
