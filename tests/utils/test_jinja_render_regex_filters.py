# st2common

import pytest

from ultron8.utils import jinja as jinja_utils


class TestJinjaUtilsRegexFilterTestCase:
    def test_filters_regex_match(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{k1 | regex_match("x")}}'
        actual = env.from_string(template).render({"k1": "xyz"})
        expected = "True"
        assert actual == expected

        template = '{{k1 | regex_match("y")}}'
        actual = env.from_string(template).render({"k1": "xyz"})
        expected = "False"
        assert actual == expected

        template = '{{k1 | regex_match("^v(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$")}}'
        actual = env.from_string(template).render({"k1": "v0.10.1"})
        expected = "True"
        assert actual == expected

    def test_filters_regex_replace(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{k1 | regex_replace("x", "y")}}'
        actual = env.from_string(template).render({"k1": "xyz"})
        expected = "yyz"
        assert actual == expected

        template = '{{k1 | regex_replace("(blue|white|red)", "color")}}'
        actual = env.from_string(template).render({"k1": "blue socks and red shoes"})
        expected = "color socks and color shoes"
        assert actual == expected

    def test_filters_regex_search(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{k1 | regex_search("x")}}'
        actual = env.from_string(template).render({"k1": "xyz"})
        expected = "True"
        assert actual == expected

        template = '{{k1 | regex_search("y")}}'
        actual = env.from_string(template).render({"k1": "xyz"})
        expected = "True"
        assert actual == expected

        template = '{{k1 | regex_search("^v(\\d+\\.)?(\\d+\\.)?(\\*|\\d+)$")}}'
        actual = env.from_string(template).render({"k1": "v0.10.1"})
        expected = "True"
        assert actual == expected

    def test_filters_regex_substring(self):
        env = jinja_utils.get_jinja_environment()

        # Normal (match)
        template = r'{{input_str | regex_substring("([0-9]{3} \w+ (?:Ave|St|Dr))")}}'
        actual = env.from_string(template).render(
            {"input_str": "My address is 123 Somewhere Ave. See you soon!"}
        )
        expected = "123 Somewhere Ave"
        assert actual == expected

        # Selecting second match explicitly
        template = r'{{input_str | regex_substring("([0-9]{3} \w+ (?:Ave|St|Dr))", 1)}}'
        actual = env.from_string(template).render(
            {
                "input_str": "Your address is 567 Elsewhere Dr. My address is 123 Somewhere Ave."
            }
        )
        expected = "123 Somewhere Ave"
        assert actual == expected

        # Selecting second match explicitly, but doesn't exist
        template = r'{{input_str | regex_substring("([0-9]{3} \w+ (?:Ave|St|Dr))", 1)}}'
        with pytest.raises(IndexError):
            actual = env.from_string(template).render(
                {"input_str": "Your address is 567 Elsewhere Dr."}
            )

        # No match
        template = r'{{input_str | regex_substring("([0-3]{3} \w+ (?:Ave|St|Dr))")}}'
        with pytest.raises(IndexError):
            actual = env.from_string(template).render(
                {"input_str": "My address is 986 Somewhere Ave. See you soon!"}
            )
