import requests

from tests.utils.utils import random_lower_string
from ultron8.api import crud

from ultron8.api.models.packs import PacksCreate
from ultron8.api.db_models.packs import Packs
from typing import Optional
from sqlalchemy.orm import Session


def create_random_packs(db: Session) -> Packs:
    shared_name = random_lower_string()
    name = shared_name
    description = random_lower_string()
    keywords = random_lower_string()
    version = random_lower_string()
    python_versions = random_lower_string()
    author = random_lower_string()
    email = "info@theblacktonystark.com"
    # contributors = [random_lower_string()]
    # files = [random_lower_string()]
    contributors = random_lower_string()
    files = random_lower_string()
    path = random_lower_string()
    ref = shared_name

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

    packs = crud.packs.create(db_session=db, packs_in=packs_in)
    return packs
