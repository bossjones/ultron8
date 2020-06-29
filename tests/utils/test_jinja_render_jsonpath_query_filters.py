# st2common

from ultron8.utils import jinja as jinja_utils


class TestJinjaUtilsJsonpathQueryTestCase:
    def test_jsonpath_query_static(self):
        env = jinja_utils.get_jinja_environment()
        obj = {
            "people": [
                {"first": "James", "last": "d"},
                {"first": "Jacob", "last": "e"},
                {"first": "Jayden", "last": "f"},
                {"missing": "different"},
            ],
            "foo": {"bar": "baz"},
        }

        template = '{{ obj | jsonpath_query("people[*].first") }}'
        actual_str = env.from_string(template).render({"obj": obj})
        actual = eval(actual_str)
        expected = ["James", "Jacob", "Jayden"]
        assert actual == expected

    def test_jsonpath_query_dynamic(self):
        env = jinja_utils.get_jinja_environment()
        obj = {
            "people": [
                {"first": "James", "last": "d"},
                {"first": "Jacob", "last": "e"},
                {"first": "Jayden", "last": "f"},
                {"missing": "different"},
            ],
            "foo": {"bar": "baz"},
        }
        query = "people[*].last"

        template = "{{ obj | jsonpath_query(query) }}"
        actual_str = env.from_string(template).render({"obj": obj, "query": query})
        actual = eval(actual_str)
        expected = ["d", "e", "f"]
        assert actual == expected

    def test_jsonpath_query_no_results(self):
        env = jinja_utils.get_jinja_environment()
        obj = {
            "people": [
                {"first": "James", "last": "d"},
                {"first": "Jacob", "last": "e"},
                {"first": "Jayden", "last": "f"},
                {"missing": "different"},
            ],
            "foo": {"bar": "baz"},
        }
        query = "query_returns_no_results"

        template = "{{ obj | jsonpath_query(query) }}"
        actual_str = env.from_string(template).render({"obj": obj, "query": query})
        actual = eval(actual_str)
        expected = None
        assert actual == expected
