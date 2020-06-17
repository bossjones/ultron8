import logging
import os
import socket

import pytest

from ultron8.utils import system_info

logger = logging.getLogger(__name__)


@pytest.mark.utilsonly
@pytest.mark.unittest
class TestLogger:
    def test_process_info(self):
        process_info = system_info.get_process_info()
        assert process_info["hostname"] == socket.gethostname()
        assert process_info["pid"] == os.getpid()
