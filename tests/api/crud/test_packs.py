from fastapi.encoders import jsonable_encoder
from freezegun import freeze_time
import pytest
from sqlalchemy.orm.session import Session

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.models.packs import PacksBase, PacksBaseInDB, PacksCreate, PacksUpdate

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


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.packsonly
@pytest.mark.unittest
def test_create_packs(db: Session) -> None:
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
    packs = crud.packs.create(db, packs_in=packs_in)
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
    assert packs.created_at == "2019-07-25 01:11:00.740428"
    assert packs.updated_at == "2019-07-25 01:11:00.740428"
    # assert hasattr(packs, "hashed_password")


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.packsonly
@pytest.mark.unittest
def test_get_packs(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    keywords = random_lower_string()
    version = random_lower_string()
    python_versions = random_lower_string()
    author = random_lower_string()
    email = "info@theblacktonystark.com"
    contributors = random_lower_string()
    files = random_lower_string()
    path = random_lower_string()
    ref = random_lower_string()

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
    packs = crud.packs.create(db, packs_in=packs_in)
    packs_2 = crud.packs.get(db, packs_id=packs.id)
    assert jsonable_encoder(packs) == jsonable_encoder(packs_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.packsonly
@pytest.mark.unittest
def test_update_packs(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    keywords = random_lower_string()
    version = random_lower_string()
    python_versions = random_lower_string()
    author = random_lower_string()
    email = "info@theblacktonystark.com"
    contributors = random_lower_string()
    files = random_lower_string()
    path = random_lower_string()
    ref = random_lower_string()

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
    packs = crud.packs.create(db, packs_in=packs_in)
    description2 = random_lower_string()
    packs_update = PacksUpdate(description=description2, files=files, path=path)
    packs2 = crud.packs.update(db_session=db, packs=packs, packs_in=packs_update)

    assert packs.name == packs2.name
    assert packs.description == description2
    assert packs.keywords == packs2.keywords
    assert packs.version == packs2.version
    assert packs.python_versions == packs2.python_versions
    assert packs.author == packs2.author
    assert packs.email == packs2.email
    assert packs.contributors == packs2.contributors
    assert packs.files == packs2.files
    assert packs.path == packs2.path
    assert packs.ref == packs2.ref
    assert packs.created_at == "2019-07-25 01:11:00.740428"
    assert packs.updated_at == "2019-07-25 01:11:00.740428"


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.packsonly
@pytest.mark.unittest
def test_delete_packs(db: Session) -> None:
    name = random_lower_string()
    description = random_lower_string()
    keywords = random_lower_string()
    version = random_lower_string()
    python_versions = random_lower_string()
    author = random_lower_string()
    email = "info@theblacktonystark.com"
    contributors = random_lower_string()
    files = random_lower_string()
    path = random_lower_string()
    ref = random_lower_string()

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
    packs = crud.packs.create(db, packs_in=packs_in)

    packs2 = crud.packs.remove(db_session=db, id=packs.id)

    packs3 = crud.packs.get(db_session=db, packs_id=packs.id)

    assert packs3 is None

    assert packs2.id == packs.id
    assert packs2.name == name
    assert packs2.description == description
    assert packs2.keywords == keywords
    assert packs2.version == version
    assert packs2.python_versions == python_versions
    assert packs2.author == author
    assert packs2.email == email
    assert packs2.contributors == contributors
    assert packs2.files == files
    assert packs2.path == path
    assert packs2.ref == ref
    assert packs2.created_at == "2019-07-25 01:11:00.740428"
    assert packs2.updated_at == "2019-07-25 01:11:00.740428"
