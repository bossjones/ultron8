# st2

from ultron8.utils.misc import rstrip_last_char
from ultron8.utils.misc import strip_shell_chars
from ultron8.utils.misc import lowercase_value
from ultron8.utils.misc import sanitize_output
from ultron8.utils.ujson import fast_deepcopy

__all__ = ["MiscUtilTestCase"]


class MiscUtilTestCase:
    def test_rstrip_last_char(self):
        assert rstrip_last_char(None, "\n") == None
        assert rstrip_last_char("stuff", None) == "stuff"
        assert rstrip_last_char("", "\n") == ""
        assert rstrip_last_char("foo", "\n") == "foo"
        assert rstrip_last_char("foo\n", "\n") == "foo"
        assert rstrip_last_char("foo\n\n", "\n") == "foo\n"
        assert rstrip_last_char("foo\r", "\r") == "foo"
        assert rstrip_last_char("foo\r\r", "\r") == "foo\r"
        assert rstrip_last_char("foo\r\n", "\r\n") == "foo"
        assert rstrip_last_char("foo\r\r\n", "\r\n") == "foo\r"
        assert rstrip_last_char("foo\n\r", "\r\n") == "foo\n\r"

    def test_strip_shell_chars(self):
        assert strip_shell_chars(None) == None
        assert strip_shell_chars("foo") == "foo"
        assert strip_shell_chars("foo\r") == "foo"
        assert strip_shell_chars("fo\ro\r") == "fo\ro"
        assert strip_shell_chars("foo\n") == "foo"
        assert strip_shell_chars("fo\no\n") == "fo\no"
        assert strip_shell_chars("foo\r\n") == "foo"
        assert strip_shell_chars("fo\no\r\n") == "fo\no"
        assert strip_shell_chars("foo\r\n\r\n") == "foo\r\n"

    def test_lowercase_value(self):
        value = "TEST"
        expected_value = "test"
        assert expected_value == lowercase_value(value=value)

        value = ["testA", "TESTb", "TESTC"]
        expected_value = ["testa", "testb", "testc"]
        assert expected_value == lowercase_value(value=value)

        value = {"testA": "testB", "testC": "TESTD", "TESTE": "TESTE"}
        expected_value = {"testa": "testb", "testc": "testd", "teste": "teste"}
        assert expected_value == lowercase_value(value=value)

    def test_fast_deepcopy_success(self):
        values = [
            "a",
            u"٩(̾●̮̮̃̾•̃̾)۶",
            1,
            [1, 2, "3", "b"],
            {"a": 1, "b": "3333", "c": "d"},
        ]
        expected_values = [
            "a",
            u"٩(̾●̮̮̃̾•̃̾)۶",
            1,
            [1, 2, "3", "b"],
            {"a": 1, "b": "3333", "c": "d"},
        ]

        for value, expected_value in zip(values, expected_values):
            result = fast_deepcopy(value)
            assert result == value
            assert result == expected_value

    def test_sanitize_output_use_pyt_false(self):
        # pty is not used, \r\n shouldn't be replaced with \n
        input_strs = [
            "foo",
            "foo\n",
            "foo\r\n",
            "foo\nbar\nbaz\n",
            "foo\r\nbar\r\nbaz\r\n",
        ]
        expected = ["foo", "foo", "foo", "foo\nbar\nbaz", "foo\r\nbar\r\nbaz"]

        for input_str, expected_output in zip(input_strs, expected):
            output = sanitize_output(input_str, uses_pty=False)
            assert expected_output == output

    def test_sanitize_output_use_pyt_true(self):
        # pty is used, \r\n should be replaced with \n
        input_strs = [
            "foo",
            "foo\n",
            "foo\r\n",
            "foo\nbar\nbaz\n",
            "foo\r\nbar\r\nbaz\r\n",
        ]
        expected = ["foo", "foo", "foo", "foo\nbar\nbaz", "foo\nbar\nbaz"]

        for input_str, expected_output in zip(input_strs, expected):
            output = sanitize_output(input_str, uses_pty=True)
            assert expected_output == output
