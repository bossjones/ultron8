"""
 Daemonize ultron8d.
"""
import contextlib
import logging.config
import os
import signal
import threading
import time

import pkg_resources

import ultron8
from ultron8.utils import chdir, flock, signals

# import ipdb

# from twisted.internet import defer
# from twisted.internet import reactor
# from twisted.python import log as twisted_log
# from ultron8.manhole import make_manhole
# from ultron8.mesos import MesosClusterRepository

log = logging.getLogger(__name__)

# SOURCE: https://docs.python.org/3.6/library/asyncio-dev.html#asyncio-dev
# SOURCE: https://docs.python.org/3.6/library/asyncio.html
# SOURCE: https://docs.python.org/3.6/library/asyncio-dev.html#asyncio-debug-mode
# FIXME: NOTE, IF DEBUG ENVIRONMENT ENABLE ASYNCIO DEBUGGING
# AbstractEventLoop.set_debug()


def setup_logging(options):
    default = pkg_resources.resource_filename(ultron8.__name__, "logging.conf")
    logfile = options.log_conf or default

    level = asyncio_level = None
    # level = None
    if options.verbose > 0:
        level = logging.INFO
        asyncio_level = logging.WARNING
    if options.verbose > 1:
        level = logging.DEBUG
        asyncio_level = logging.INFO
    if options.verbose > 2:
        asyncio_level = logging.DEBUG

    ultron8_logger = logging.getLogger("ultron8")
    asyncio_logger = logging.getLogger("asyncio")

    logging.config.fileConfig(logfile)
    if level is not None:
        ultron8_logger.setLevel(level)
    if asyncio_level is not None:
        asyncio_logger.setLevel(asyncio_level)

    # Hookup twisted to standard logging
    # twisted_log.PythonLoggingObserver().start()

    # Show stack traces for errors in twisted deferreds.
    # if options.debug:
    #     defer.setDebugging(True)


@contextlib.contextmanager
def no_daemon_context(workdir, lockfile=None, signal_map={}):
    with chdir(workdir), flock(lockfile), signals(signal_map):
        yield


# class TronDaemon(object):
#     """Daemonize and run the ultron8 daemon."""

#     def __init__(self, options):
#         self.options = options
#         setup_logging(self.options)

#         self.mcp = None
#         self.lock_file = self.options.lock_file
#         self.working_dir = self.options.working_dir
#         self.signals = {signal.SIGINT: signal.default_int_handler}
#         self.manhole_sock = f"{self.options.working_dir}/manhole.sock"

#     def run(self):
#         with no_daemon_context(self.working_dir, self.lock_file, self.signals):
#             signal_map = {
#                 signal.SIGHUP: self._handle_reconfigure,
#                 signal.SIGINT: self._handle_shutdown,
#                 signal.SIGTERM: self._handle_shutdown,
#                 signal.SIGQUIT: self._handle_shutdown,
#                 signal.SIGUSR1: self._handle_debug,
#             }
#             signal.pthread_sigmask(signal.SIG_BLOCK, signal_map.keys())

#             self._run_mcp()
#             self._run_www_api()
#             self._run_manhole()
#             self._run_reactor()

#             while True:
#                 signum = signal.sigwait(list(signal_map.keys()))
#                 if signum in signal_map:
#                     logging.info(f"Got signal {str(signum)}")
#                     signal_map[signum](signum, None)

#     def _run_manhole(self):
#         # This condition is made with the assumption that no existing daemon
#         # is running. If there is one, the following code could potentially
#         # cause problems for the other daemon by removing its socket.
#         if os.path.exists(self.manhole_sock):
#             log.info('Removing orphaned manhole socket')
#             os.remove(self.manhole_sock)

#         self.manhole = make_manhole(dict(ultron8d=self, mcp=self.mcp))
#         reactor.listenUNIX(self.manhole_sock, self.manhole)
#         log.info(f"manhole started on {self.manhole_sock}")

#     def _run_www_api(self):
#         # Local import required because of reactor import in server and www
#         from ultron8.api import resource
#         site = resource.TronSite.create(self.mcp, self.options.web_path)
#         port = self.options.listen_port
#         reactor.listenTCP(port, site, interface=self.options.listen_host)

#     def _run_mcp(self):
#         # Local import required because of reactor import in mcp
#         from ultron8 import mcp
#         working_dir = self.options.working_dir
#         config_path = self.options.config_path
#         self.mcp = mcp.MasterControlProgram(working_dir, config_path)

#         try:
#             self.mcp.initial_setup()
#         except Exception as e:
#             msg = "Error in configuration %s: %s"
#             log.exception(msg % (config_path, e))
#             raise

#     def _run_reactor(self):
#         """Run the twisted reactor."""
#         threading.Thread(
#             target=reactor.run,
#             daemon=True,
#             kwargs=dict(installSignalHandlers=0)
#         ).start()

#     def _handle_shutdown(self, sig_num, stack_frame):
#         log.info(f"Shutdown requested via {str(sig_num)}")
#         reactor.callLater(0, reactor.stop)
#         waited = 0
#         while reactor.running:
#             if waited > 5:
#                 log.error("timed out waiting for reactor shutdown")
#                 break
#             time.sleep(0.1)
#             waited += 0.1
#         if self.mcp:
#             self.mcp.shutdown()
#         MesosClusterRepository.shutdown()
#         raise SystemExit(f"Terminating on signal {str(sig_num)}")

#     def _handle_reconfigure(self, _signal_number, _stack_frame):
#         log.info("Reconfigure requested by SIGHUP.")
#         reactor.callLater(0, self.mcp.reconfigure)

#     def _handle_debug(self, _signal_number, _stack_frame):
#         ipdb.set_trace()
