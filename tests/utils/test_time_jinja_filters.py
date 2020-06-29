# st2

from ultron8.expressions.functions import time
import pytest


class TestTimeJinjaFilters:
    def test_to_human_time_from_seconds(self):
        assert "0s" == time.to_human_time_from_seconds(seconds=0)
        assert "0.1\u03BCs" == time.to_human_time_from_seconds(seconds=0.1)
        assert "56s" == time.to_human_time_from_seconds(seconds=56)
        assert "56s" == time.to_human_time_from_seconds(seconds=56.2)
        assert "7m36s" == time.to_human_time_from_seconds(seconds=456)
        assert "1h16m0s" == time.to_human_time_from_seconds(seconds=4560)
        assert "1y12d16h36m37s" == time.to_human_time_from_seconds(seconds=45678997)
        with pytest.raises(AssertionError):
            time.to_human_time_from_seconds(seconds="stuff")
