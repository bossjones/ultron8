# st2common

from ultron8.utils import jinja as jinja_utils


class TestJinjaUtilsPathFilterTestCase:
    def test_basename(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{k1 | basename}}"
        actual = env.from_string(template).render({"k1": "/some/path/to/file.txt"})
        assert actual == "file.txt"

        actual = env.from_string(template).render({"k1": "/some/path/to/dir"})
        assert actual == "dir"

        actual = env.from_string(template).render({"k1": "/some/path/to/dir/"})
        assert actual == ""

    def test_dirname(self):
        env = jinja_utils.get_jinja_environment()

        template = "{{k1 | dirname}}"
        actual = env.from_string(template).render({"k1": "/some/path/to/file.txt"})
        assert actual == "/some/path/to"

        actual = env.from_string(template).render({"k1": "/some/path/to/dir"})
        assert actual == "/some/path/to"

        actual = env.from_string(template).render({"k1": "/some/path/to/dir/"})
        assert actual == "/some/path/to/dir"
