import logging

from peavy.middleware import RequestLoggingMiddleware

class BasicFilter(logging.Filter):
    """
    Adds basic request info (unique ID, user, client IP) into the log record.
    """

    def filter(self, record):
        request = RequestLoggingMiddleware.context.request

        record.uuid = getattr(request, "uuid", "?")
        record.user = getattr(request, "user", "?")
        meta = getattr(request, "META", {})
        record.client_ip = meta.get("REMOTE_ADDR", "?")
        return True

class MetaFilter(logging.Filter):
    """
    Adds all the request metadata to the log record.
    """

    def filter(self, record):
        request = RequestLoggingMiddleware.context.request

        meta = getattr(request, "META", {})
        for key, value in meta.items():
            if hasattr(record, key):
                continue
            setattr(record, "META_" + key, value)

        return True

