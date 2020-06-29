from ultron8.utils import jinja as jinja_utils


class JinjaUtilsRenderTestCase:
    def test_render_values(self):
        actual = jinja_utils.render_values(
            mapping={"k1": "{{a}}", "k2": "{{b}}"}, context={"a": "v1", "b": "v2"}
        )
        expected = {"k2": "v2", "k1": "v1"}
        assert actual == expected

    def test_render_values_skip_missing(self):
        actual = jinja_utils.render_values(
            mapping={"k1": "{{a}}", "k2": "{{b}}", "k3": "{{c}}"},
            context={"a": "v1", "b": "v2"},
            allow_undefined=True,
        )
        expected = {"k2": "v2", "k1": "v1", "k3": ""}
        assert actual == expected

    def test_render_values_ascii_and_unicode_values(self):
        mapping = {
            u"k_ascii": "{{a}}",
            u"k_unicode": "{{b}}",
            u"k_ascii_unicode": "{{c}}",
        }
        context = {
            "a": u"some ascii value",
            "b": u"٩(̾●̮̮̃̾•̃̾)۶ ٩(̾●̮̮̃̾•̃̾)۶ ćšž",
            "c": u"some ascii some ٩(̾●̮̮̃̾•̃̾)۶ ٩(̾●̮̮̃̾•̃̾)۶ ",
        }

        expected = {
            "k_ascii": u"some ascii value",
            "k_unicode": u"٩(̾●̮̮̃̾•̃̾)۶ ٩(̾●̮̮̃̾•̃̾)۶ ćšž",
            "k_ascii_unicode": u"some ascii some ٩(̾●̮̮̃̾•̃̾)۶ ٩(̾●̮̮̃̾•̃̾)۶ ",
        }

        actual = jinja_utils.render_values(
            mapping=mapping, context=context, allow_undefined=True
        )

        assert actual == expected

    def test_convert_str_to_raw(self):
        jinja_expr = "{{foobar}}"
        expected_raw_block = "{% raw %}{{foobar}}{% endraw %}"
        assert expected_raw_block == jinja_utils.convert_jinja_to_raw_block(jinja_expr)

        jinja_block_expr = "{% for item in items %}foobar{% end for %}"
        expected_raw_block = (
            "{% raw %}{% for item in items %}foobar{% end for %}{% endraw %}"
        )
        assert expected_raw_block == jinja_utils.convert_jinja_to_raw_block(
            jinja_block_expr
        )

    def test_convert_list_to_raw(self):
        jinja_expr = [
            "foobar",
            "{{foo}}",
            "{{bar}}",
            "{% for item in items %}foobar{% end for %}",
            {"foobar": "{{foobar}}"},
        ]

        expected_raw_block = [
            "foobar",
            "{% raw %}{{foo}}{% endraw %}",
            "{% raw %}{{bar}}{% endraw %}",
            "{% raw %}{% for item in items %}foobar{% end for %}{% endraw %}",
            {"foobar": "{% raw %}{{foobar}}{% endraw %}"},
        ]

        assert expected_raw_block == jinja_utils.convert_jinja_to_raw_block(jinja_expr)

    def test_convert_dict_to_raw(self):
        jinja_expr = {
            "var1": "foobar",
            "var2": ["{{foo}}", "{{bar}}"],
            "var3": {"foobar": "{{foobar}}"},
            "var4": {"foobar": "{% for item in items %}foobar{% end for %}"},
        }

        expected_raw_block = {
            "var1": "foobar",
            "var2": ["{% raw %}{{foo}}{% endraw %}", "{% raw %}{{bar}}{% endraw %}"],
            "var3": {"foobar": "{% raw %}{{foobar}}{% endraw %}"},
            "var4": {
                "foobar": "{% raw %}{% for item in items %}foobar{% end for %}{% endraw %}"
            },
        }

        assert expected_raw_block == jinja_utils.convert_jinja_to_raw_block(jinja_expr)
