# st2common

from ultron8.utils import jinja as jinja_utils


class TestJinjaUtilsVersionsFilterTestCase:
    def test_version_compare(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{version | version_compare("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.9.0"})
        expected = "-1"
        assert actual == expected

        template = '{{version | version_compare("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "1"
        assert actual == expected

        template = '{{version | version_compare("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.0"})
        expected = "0"
        assert actual == expected

    def test_version_more_than(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{version | version_more_than("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.9.0"})
        expected = "False"
        assert actual == expected

        template = '{{version | version_more_than("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "True"
        assert actual == expected

        template = '{{version | version_more_than("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.0"})
        expected = "False"
        assert actual == expected

    def test_version_less_than(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{version | version_less_than("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.9.0"})
        expected = "True"
        assert actual == expected

        template = '{{version | version_less_than("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "False"
        assert actual == expected

        template = '{{version | version_less_than("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.0"})
        expected = "False"
        assert actual == expected

    def test_version_equal(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{version | version_equal("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.9.0"})
        expected = "False"
        assert actual == expected

        template = '{{version | version_equal("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "False"
        assert actual == expected

        template = '{{version | version_equal("0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.0"})
        expected = "True"
        assert actual == expected

    def test_version_match(self):
        env = jinja_utils.get_jinja_environment()

        template = '{{version | version_match(">0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "True"
        assert actual == expected
        actual = env.from_string(template).render({"version": "0.1.1"})
        expected = "False"
        assert actual == expected

        template = '{{version | version_match("<0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.1.0"})
        expected = "True"
        assert actual == expected
        actual = env.from_string(template).render({"version": "1.1.0"})
        expected = "False"
        assert actual == expected

        template = '{{version | version_match("==0.10.0")}}'
        actual = env.from_string(template).render({"version": "0.10.0"})
        expected = "True"
        assert actual == expected
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "False"
        assert actual == expected

    def test_version_bump_major(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{version | version_bump_major}}"
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "1.0.0"
        assert actual == expected

    def test_version_bump_minor(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{version | version_bump_minor}}"
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "0.11.0"
        assert actual == expected

    def test_version_bump_patch(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{version | version_bump_patch}}"
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "0.10.2"
        assert actual == expected

    def test_version_strip_patch(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{version | version_strip_patch}}"
        actual = env.from_string(template).render({"version": "0.10.1"})
        expected = "0.10"
        assert actual == expected
