# st2

from ultron8.utils import jinja as jinja_utils
import pytest


class JinjaUtilsTimeFilterTestCase:
    def test_to_human_time_filter(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{k1 | to_human_time_from_seconds}}"
        actual = env.from_string(template).render({"k1": 12345})
        assert actual == "3h25m45s"

        actual = env.from_string(template).render({"k1": 0})
        assert actual == "0s"

        with pytest.raises(AssertionError):
            env.from_string(template).render({"k1": "stuff"})
