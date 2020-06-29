# st2common

from ultron8.utils import jinja as jinja_utils


class JinjaUtilsJsonEscapeTestCase:
    def test_doublequotes(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": 'foo """ bar'})
        expected = 'foo \\"\\"\\" bar'
        assert actual == expected

    def test_backslashes(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": r"foo \ bar"})
        expected = "foo \\\\ bar"
        assert actual == expected

    def test_backspace(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": "foo \b bar"})
        expected = "foo \\b bar"
        assert actual == expected

    def test_formfeed(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": "foo \f bar"})
        expected = "foo \\f bar"
        assert actual == expected

    def test_newline(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": "foo \n bar"})
        expected = "foo \\n bar"
        assert actual == expected

    def test_carriagereturn(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": "foo \r bar"})
        expected = "foo \\r bar"
        assert actual == expected

    def test_tab(self):
        env = jinja_utils.get_jinja_environment()
        template = "{{ test_str | json_escape }}"
        actual = env.from_string(template).render({"test_str": "foo \t bar"})
        expected = "foo \\t bar"
        assert actual == expected
