import os
import socket

__all__ = ["get_host_info", "get_process_info"]


def get_host_info():
    host_info = {"hostname": socket.gethostname()}
    return host_info


def get_process_info():
    process_info = {"hostname": socket.gethostname(), "pid": os.getpid()}
    return process_info
