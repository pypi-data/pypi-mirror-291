import threading
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y %m %d %H:%M:%S",
    level=logging.INFO,
)


def threaded(fn):
    """A wrapper for a threaded function

    Args:
        fn (function): function to be threaded
    """

    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper
