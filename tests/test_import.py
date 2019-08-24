#!/usr/bin/env python
import pytest
from pytest import approx
from pytest import raises


def test() -> None:
    import ultron8

    pass


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
