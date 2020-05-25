import datetime
from datetime import timedelta
import logging

from typing import Tuple

# import jwt as pyjwt
from freezegun import freeze_time
from jose import jwt as josejwt
import pytest
from sqlalchemy.orm import Session

import ultron8
from ultron8.api import crud, settings
from ultron8.api.core import jwt

from tests.conftest import fixtures_path

logger = logging.getLogger(__name__)


@freeze_time("2012-01-14 03:21:34", tz_offset=-4)
@pytest.mark.jwtonly
@pytest.mark.unittest
class TestCreateAccessToken(object):
    # def test_create_access_token(
    #     self, first_superuser_username_and_password_fixtures, db
    # ):
    #     username, password = first_superuser_username_and_password_fixtures
    #     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    #     user = crud.user.authenticate(db, email=username, password=password)

    #     a_token = jwt.create_access_token(
    #         data={"user_id": user.id}, expires_delta=access_token_expires
    #     )

    #     expire_expected = datetime.datetime.utcnow() + access_token_expires

    #     test_data = {"user_id": user.id, "exp": expire_expected, "sub": "access"}

    #     expected_token = pyjwt.encode(test_data, settings.SECRET_KEY, algorithm="HS256")

    #     assert a_token == expected_token

    # def test_create_access_token_without_timedelta(
    #     self, first_superuser_username_and_password_fixtures, db
    # ):
    #     username, password = first_superuser_username_and_password_fixtures

    #     user = crud.user.authenticate(db, email=username, password=password)

    #     a_token = jwt.create_access_token(data={"user_id": user.id})

    #     expire_expected = datetime.datetime.utcnow() + timedelta(minutes=15)

    #     test_data = {"user_id": user.id, "exp": expire_expected, "sub": "access"}

    #     expected_token = pyjwt.encode(test_data, settings.SECRET_KEY, algorithm="HS256")

    #     assert a_token == expected_token

    def test_create_access_token2(
        self,
        first_superuser_username_and_password_fixtures: Tuple[str, str],
        db: Session,
    ) -> None:
        username, password = first_superuser_username_and_password_fixtures

        FIXTURE_ACCESS_TOKEN_EXPIRE_MINUTES = (
            60 * 24 * 2
        )  # 60 minutes * 24 hours * 2 days = 2 days
        access_token_expires = timedelta(minutes=FIXTURE_ACCESS_TOKEN_EXPIRE_MINUTES)

        user = crud.user.authenticate(db, email=username, password=password)

        a_token = jwt.create_access_token(user.id, expires_delta=access_token_expires)

        expire_expected = datetime.datetime.utcnow() + access_token_expires

        test_data = {"exp": expire_expected, "sub": str(user.id)}

        expected_token = josejwt.encode(
            test_data, settings.SECRET_KEY, algorithm="HS256"
        )

        assert a_token == expected_token

    def test_create_access_token_without_timedelta2(
        self,
        first_superuser_username_and_password_fixtures: Tuple[str, str],
        db: Session,
    ) -> None:
        username, password = first_superuser_username_and_password_fixtures

        user = crud.user.authenticate(db, email=username, password=password)

        a_token = jwt.create_access_token(user.id)

        expire_expected = datetime.datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        test_data = {"exp": expire_expected, "sub": str(user.id)}

        expected_token = josejwt.encode(
            test_data, settings.SECRET_KEY, algorithm="HS256"
        )

        assert a_token == expected_token
