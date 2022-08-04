# from ultron8.api.repositories.repo_user import CRUDUser

from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from ultron8.api.core.security import get_password_hash, verify_password
from ultron8.api.db_models.user import User
from ultron8.api.factories.users import _MakeRandomNormalUserFactory
from ultron8.api.models.user import UserCreate, UserUpdate
from ultron8.api.repositories.repo_user import user as repository_user

from tests.utils.utils import get_server_api, random_email, random_lower_string


def test_create_user(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user_in = UserCreate(email=email, password=password)
    user = repository_user.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user_in = UserCreate(email=email, password=password)
    user = repository_user.create(db, obj_in=user_in)
    authenticated_user = repository_user.authenticate(
        db, email=email, password=password
    )
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user = repository_user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user_in = UserCreate(email=email, password=password)
    user = repository_user.create(db, obj_in=user_in)
    is_active = repository_user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user_in = UserCreate(email=email, password=password, disabled=True)
    user = repository_user.create(db, obj_in=user_in)
    is_active = repository_user.is_active(user)
    assert is_active


def test_check_if_user_is_superuser(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = repository_user.create(db, obj_in=user_in)
    is_superuser = repository_user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = repository_user.create(db, obj_in=user_in)
    is_superuser = repository_user.is_superuser(user)
    assert is_superuser is False


def test_get_user(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    username = data.email
    password = data.password
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = repository_user.create(db, obj_in=user_in)
    user_2 = repository_user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    data = _MakeRandomNormalUserFactory()
    email = data.email
    password = data.password
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = repository_user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    repository_user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = repository_user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
