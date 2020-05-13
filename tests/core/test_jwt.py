import logging
import datetime
from datetime import timedelta
import os
import pytest
from tests.conftest import fixtures_path
import ultron8
from ultron8.api import settings
from ultron8.api import crud
from ultron8.api.core import jwt

import jwt as pyjwt

from freezegun import freeze_time

logger = logging.getLogger(__name__)


@freeze_time("2012-01-14 03:21:34", tz_offset=-4)
@pytest.mark.jwtonly
@pytest.mark.unittest
class TestCreateAccessToken(object):
    def test_create_access_token(
        self, first_superuser_username_and_password_fixtures, db
    ):
        username, password = first_superuser_username_and_password_fixtures
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        user = crud.user.authenticate(db, email=username, password=password)

        a_token = jwt.create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )

        expire_expected = datetime.datetime.utcnow() + access_token_expires

        test_data = {"user_id": user.id, "exp": expire_expected, "sub": "access"}

        expected_token = pyjwt.encode(test_data, settings.SECRET_KEY, algorithm="HS256")

        assert a_token == expected_token
