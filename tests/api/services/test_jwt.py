from datetime import timedelta

import jwt
import pytest

# from app.models.domain.users import UserInDB
from ultron8.api.models.user import UserInDB
from ultron8.api.services.jwt import (
    ALGORITHM,
    create_access_token_for_user,
    create_jwt_token,
    get_email_from_token,
)


@pytest.mark.unittest
@pytest.mark.jwtonly
def test_creating_jwt_token() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    parsed_payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])

    assert parsed_payload["content"] == "payload"


@pytest.mark.unittest
@pytest.mark.jwtonly
def test_creating_token_for_user(test_user: UserInDB) -> None:
    token = create_access_token_for_user(user=test_user, secret_key="secret")
    parsed_payload = jwt.decode(token, "secret", algorithms=[ALGORITHM])

    assert parsed_payload["email"] == test_user.email


@pytest.mark.unittest
@pytest.mark.jwtonly
def test_retrieving_token_from_user(test_user: UserInDB) -> None:
    token = create_access_token_for_user(user=test_user, secret_key="secret")
    email = get_email_from_token(token, "secret")
    assert email == test_user.email


@pytest.mark.unittest
@pytest.mark.jwtonly
def test_error_when_wrong_token() -> None:
    with pytest.raises(ValueError):
        get_email_from_token("asdf", "asdf")


@pytest.mark.unittest
@pytest.mark.jwtonly
def test_error_when_wrong_token_shape() -> None:
    token = create_jwt_token(
        jwt_content={"content": "payload"},
        secret_key="secret",
        expires_delta=timedelta(minutes=1),
    )
    with pytest.raises(ValueError):
        get_email_from_token(token, "secret")
