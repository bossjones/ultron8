import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.packs import PacksBase
from ultron8.api.models.packs import PacksBaseInDB
from ultron8.api.models.packs import PacksCreate
from ultron8.api.models.packs import PacksUpdate

# pack_linux = Packs(
#     name="linux",
#     description="Generic Linux actions",
#     keywords="linux",
#     version="0.1.0",
#     python_versions="3",
#     author="Jarvis",
#     email="info@theblacktonystark.com",
#     contributors="bossjones",
#     files="./tests/fixtures/simple/packs/linux",
#     path="./tests/fixtures/simple/packs/linux",
#     ref="linux"
# )

# pack_linux


@pytest.mark.packsonly
@pytest.mark.unittest
def test_create_packs():
    name = "linuxtest"
    description = "TEST Generic Linux actions"
    keywords = "linux"
    version = "0.1.0"
    python_versions = "3"
    author = "Jarvis"
    email = "info@theblacktonystark.com"
    contributors = "bossjones"
    files = "./tests/fixtures/simple/packs/linux"
    path = "./tests/fixtures/simple/packs/linux"
    ref = "linux"

    packs_in = PacksCreate(
        name=name,
        description=description,
        keywords=keywords,
        version=version,
        python_versions=python_versions,
        author=author,
        email=email,
        contributors=contributors,
        files=files,
        path=path,
        ref=ref,
    )
    packs = crud.packs.create(db_session, packs_in=packs_in)
    assert packs.name == name
    assert packs.description == description
    assert packs.keywords == keywords
    assert packs.version == version
    assert packs.python_versions == python_versions
    assert packs.author == author
    assert packs.email == email
    assert packs.contributors == contributors
    assert packs.files == files
    assert packs.path == path
    assert packs.ref == ref
    # assert hasattr(packs, "hashed_password")


# def test_authenticate_packs():
#     email = random_lower_string()
#     password = random_lower_string()
#     packs_in = PacksCreate(email=email, password=password)
#     packs = crud.packs.create(db_session, packs_in=packs_in)
#     authenticated_packs = crud.packs.authenticate(
#         db_session, email=email, password=password
#     )
#     assert authenticated_packs
#     assert packs.email == authenticated_packs.email


# def test_not_authenticate_packs():
#     email = random_lower_string()
#     password = random_lower_string()
#     packs = crud.packs.authenticate(db_session, email=email, password=password)
#     assert packs is None


# def test_check_if_packs_is_active():
#     email = random_lower_string()
#     password = random_lower_string()
#     packs_in = PacksCreate(email=email, password=password)
#     packs = crud.packs.create(db_session, packs_in=packs_in)
#     is_active = crud.packs.is_active(packs)
#     assert is_active is True


# def test_check_if_packs_is_active_inactive():
#     email = random_lower_string()
#     password = random_lower_string()
#     packs_in = PacksCreate(email=email, password=password, disabled=True)
#     print(packs_in)
#     packs = crud.packs.create(db_session, packs_in=packs_in)
#     print(packs)
#     is_active = crud.packs.is_active(packs)
#     print(is_active)
#     assert is_active


# def test_check_if_packs_is_superpacks():
#     email = random_lower_string()
#     password = random_lower_string()
#     packs_in = PacksCreate(email=email, password=password, is_superpacks=True)
#     packs = crud.packs.create(db_session, packs_in=packs_in)
#     is_superpacks = crud.packs.is_superpacks(packs)
#     assert is_superpacks is True


# def test_check_if_packs_is_superpacks_normal_packs():
#     packsname = random_lower_string()
#     password = random_lower_string()
#     packs_in = PacksCreate(email=packsname, password=password)
#     packs = crud.packs.create(db_session, packs_in=packs_in)
#     is_superpacks = crud.packs.is_superpacks(packs)
#     assert is_superpacks is False


# def test_get_packs():
#     password = random_lower_string()
#     packsname = random_lower_string()
#     packs_in = PacksCreate(email=packsname, password=password, is_superpacks=True)
#     packs = crud.packs.create(db_session, packs_in=packs_in)
#     packs_2 = crud.packs.get(db_session, packs_id=packs.id)
#     assert packs.email == packs_2.email
#     assert jsonable_encoder(packs) == jsonable_encoder(packs_2)
