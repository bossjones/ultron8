# st2common
import json

import pytest

from ultron8.utils.casts import get_cast


class CastsTestCase:
    def test_cast_string(self):
        cast_func = get_cast("string")

        value = "test1"
        result = cast_func(value)
        assert result == "test1"

        value = u"test2"
        result = cast_func(value)
        assert result == u"test2"

        value = ""
        result = cast_func(value)
        assert result == ""

        # None should be preserved
        value = None
        result = cast_func(value)
        assert result == None

        # Non string or non, should throw a friendly exception
        value = []
        expected_msg = r'Value "\[\]" must either be a string or None. Got "list"'
        with pytest.raises(ValueError, match=expected_msg):
            cast_func(value)

    def test_cast_array(self):
        cast_func = get_cast("array")

        # Python literal
        value = str([1, 2, 3])
        result = cast_func(value)
        assert result == [1, 2, 3]

        # JSON serialized
        value = json.dumps([4, 5, 6])
        result = cast_func(value)
        assert result == [4, 5, 6]

        # Can't cast, should throw
        value = "\\invalid"
        with pytest.raises(SyntaxError):
            cast_func(value)
