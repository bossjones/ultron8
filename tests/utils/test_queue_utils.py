# st2common
import re

import pytest

import ultron8.utils.queues as queue_utils


class TestQueueUtils:
    def test_get_queue_name(self):
        with pytest.raises(ValueError):
            queue_utils.get_queue_name(queue_name_base=None, queue_name_suffix=None)
        with pytest.raises(ValueError):
            queue_utils.get_queue_name(queue_name_base="", queue_name_suffix=None)
        assert (
            queue_utils.get_queue_name(
                queue_name_base="u8.test.watch", queue_name_suffix=None
            )
            == "u8.test.watch"
        )
        assert (
            queue_utils.get_queue_name(
                queue_name_base="u8.test.watch", queue_name_suffix=""
            )
            == "u8.test.watch"
        )
        queue_name = queue_utils.get_queue_name(
            queue_name_base="u8.test.watch",
            queue_name_suffix="foo",
            add_random_uuid_to_suffix=True,
        )
        pattern = re.compile(r"u8.test.watch.foo-\w")
        assert re.match(pattern, queue_name)

        queue_name = queue_utils.get_queue_name(
            queue_name_base="u8.test.watch",
            queue_name_suffix="foo",
            add_random_uuid_to_suffix=False,
        )
        assert queue_name == "u8.test.watch.foo"
