# Copyright 2019 Extreme Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test u8client session"""
# pylint: disable=protected-access
import logging

import pytest

from ultron8.utils.pack import normalize_pack_version
from ultron8.utils.versioning import complex_semver_match

logger = logging.getLogger(__name__)


@pytest.mark.packsonly
@pytest.mark.unittest
class TestVersioningUtils:
    def test_complex_semver_match(self):
        # Positive test case
        assert complex_semver_match("1.6.0", ">=1.6.0, <2.2.0")
        assert complex_semver_match("1.6.1", ">=1.6.0, <2.2.0")
        assert complex_semver_match("2.0.0", ">=1.6.0, <2.2.0")
        assert complex_semver_match("2.1.0", ">=1.6.0, <2.2.0")
        assert complex_semver_match("2.1.9", ">=1.6.0, <2.2.0")

        assert complex_semver_match("1.6.0", "all")
        assert complex_semver_match("1.6.1", "all")
        assert complex_semver_match("2.0.0", "all")
        assert complex_semver_match("2.1.0", "all")

        assert complex_semver_match("1.6.0", ">=1.6.0")
        assert complex_semver_match("1.6.1", ">=1.6.0")
        assert complex_semver_match("2.1.0", ">=1.6.0")

        # Negative test case
        assert not complex_semver_match("1.5.0", ">=1.6.0, <2.2.0")
        assert not complex_semver_match("0.1.0", ">=1.6.0, <2.2.0")
        assert not complex_semver_match("2.2.1", ">=1.6.0, <2.2.0")
        assert not complex_semver_match("2.3.0", ">=1.6.0, <2.2.0")
        assert not complex_semver_match("3.0.0", ">=1.6.0, <2.2.0")

        assert not complex_semver_match("1.5.0", ">=1.6.0")
        assert not complex_semver_match("0.1.0", ">=1.6.0")
        assert not complex_semver_match("1.5.9", ">=1.6.0")

    def test_normalize_pack_version(self):
        # Already a valid semver version string
        assert normalize_pack_version("0.2.0") == "0.2.0"
        assert normalize_pack_version("0.2.1") == "0.2.1"
        assert normalize_pack_version("1.2.1") == "1.2.1"

        # Not a valid semver version string
        assert normalize_pack_version("0.2") == "0.2.0"
        assert normalize_pack_version("0.3") == "0.3.0"
        assert normalize_pack_version("1.3") == "1.3.0"
        assert normalize_pack_version("2.0") == "2.0.0"
