#!/usr/bin/env python
import pytest
from pytest import approx, raises


def test() -> None:
    import ultron8


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
