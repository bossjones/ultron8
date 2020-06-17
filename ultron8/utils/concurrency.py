"""
Module which acts as a compatibility later between eventlet and gevent.

It dispatches function call to the concurrency library which is configured using
"set_concurrency_library" functoion.
"""

try:
    import eventlet  # pylint: disable=import-error
except ImportError:
    eventlet = None

try:
    import gevent  # pylint: disable=import-error
    import gevent.pool
except ImportError:
    gevent = None

CONCURRENCY_LIBRARY = "eventlet"

__all__ = [
    "set_concurrency_library",
    "get_concurrency_library",
    "get_subprocess_module",
    "subprocess_popen",
    "spawn",
    "wait",
    "cancel",
    "kill",
    "sleep",
    "get_greenlet_exit_exception_class",
    "get_green_pool_class",
    "is_green_pool_free",
    "green_pool_wait_all",
]


def set_concurrency_library(library):
    global CONCURRENCY_LIBRARY

    if library not in ["eventlet", "gevent"]:
        raise ValueError("Unsupported concurrency library: %s" % (library))

    CONCURRENCY_LIBRARY = library


def get_concurrency_library():
    global CONCURRENCY_LIBRARY
    return CONCURRENCY_LIBRARY


def get_subprocess_module():
    if CONCURRENCY_LIBRARY == "eventlet":
        from eventlet.green import subprocess  # pylint: disable=import-error

        return subprocess
    elif CONCURRENCY_LIBRARY == "gevent":
        from gevent import subprocess  # pylint: disable=import-error

        return subprocess


def subprocess_popen(*args, **kwargs):
    if CONCURRENCY_LIBRARY == "eventlet":
        from eventlet.green import subprocess  # pylint: disable=import-error

        return subprocess.Popen(*args, **kwargs)
    elif CONCURRENCY_LIBRARY == "gevent":
        from gevent import subprocess  # pylint: disable=import-error

        return subprocess.Popen(*args, **kwargs)


def spawn(func, *args, **kwargs):
    if CONCURRENCY_LIBRARY == "eventlet":
        return eventlet.spawn(func, *args, **kwargs)
    elif CONCURRENCY_LIBRARY == "gevent":
        return gevent.spawn(func, *args, **kwargs)
    else:
        raise ValueError("Unsupported concurrency library")


def wait(green_thread, *args, **kwargs):
    if CONCURRENCY_LIBRARY == "eventlet":
        return green_thread.wait(*args, **kwargs)
    elif CONCURRENCY_LIBRARY == "gevent":
        return green_thread.join(*args, **kwargs)
    else:
        raise ValueError("Unsupported concurrency library")


def cancel(green_thread, *args, **kwargs):
    if CONCURRENCY_LIBRARY == "eventlet":
        return green_thread.cancel(*args, **kwargs)
    elif CONCURRENCY_LIBRARY == "gevent":
        return green_thread.kill(*args, **kwargs)
    else:
        raise ValueError("Unsupported concurrency library")


def kill(green_thread, *args, **kwargs):
    if CONCURRENCY_LIBRARY == "eventlet":
        return green_thread.kill(*args, **kwargs)
    elif CONCURRENCY_LIBRARY == "gevent":
        return green_thread.kill(*args, **kwargs)
    else:
        raise ValueError("Unsupported concurrency library")


def sleep(*args, **kwargs):
    if CONCURRENCY_LIBRARY == "eventlet":
        return eventlet.sleep(*args, **kwargs)
    elif CONCURRENCY_LIBRARY == "gevent":
        return gevent.sleep(*args, **kwargs)
    else:
        raise ValueError("Unsupported concurrency library")


def get_greenlet_exit_exception_class():
    if CONCURRENCY_LIBRARY == "eventlet":
        return eventlet.support.greenlets.GreenletExit
    elif CONCURRENCY_LIBRARY == "gevent":
        return gevent.GreenletExit
    else:
        raise ValueError("Unsupported concurrency library")


def get_green_pool_class():
    if CONCURRENCY_LIBRARY == "eventlet":
        return eventlet.GreenPool
    elif CONCURRENCY_LIBRARY == "gevent":
        return gevent.pool.Pool
    else:
        raise ValueError("Unsupported concurrency library")


def is_green_pool_free(pool):
    """
    Return True if the provided green pool is free, False otherwise.
    """
    if CONCURRENCY_LIBRARY == "eventlet":
        return pool.free()
    elif CONCURRENCY_LIBRARY == "gevent":
        return not pool.full()
    else:
        raise ValueError("Unsupported concurrency library")


def green_pool_wait_all(pool):
    """
    Wait for all the green threads in the pool to finish.
    """
    if CONCURRENCY_LIBRARY == "eventlet":
        return pool.waitall()
    elif CONCURRENCY_LIBRARY == "gevent":
        # NOTE: This mimicks eventlet.waitall() functionallity better than
        # pool.join()
        return all(gl.ready() for gl in pool.greenlets)
    else:
        raise ValueError("Unsupported concurrency library")
