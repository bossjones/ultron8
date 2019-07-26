import pytest
from fastapi.encoders import jsonable_encoder

from tests.utils.utils import random_lower_string
from ultron8.api import crud
from ultron8.api.db.u_sqlite.session import db_session
from ultron8.api.models.action import RunnerTypeModel
from ultron8.api.models.action import ActionBase
from ultron8.api.models.action import ActionBaseInDB
from ultron8.api.models.action import ActionCreate
from ultron8.api.models.action import ActionUpdate

from ultron8.api.models.packs import PacksBase
from ultron8.api.models.packs import PacksBaseInDB
from ultron8.api.models.packs import PacksCreate
from ultron8.api.models.packs import PacksUpdate

from freezegun import freeze_time


# def test_create_action():
#     email = random_lower_string()
#     password = random_lower_string()
#     action_in = UserCreate(email=email, password=password)
#     action = crud.action.create(db_session, action_in=action_in)
#     assert action.email == email
#     assert hasattr(action, "hashed_password")


# def test_authenticate_action():
#     email = random_lower_string()
#     password = random_lower_string()
#     action_in = UserCreate(email=email, password=password)
#     action = crud.action.create(db_session, action_in=action_in)
#     authenticated_action = crud.action.authenticate(
#         db_session, email=email, password=password
#     )
#     assert authenticated_action
#     assert action.email == authenticated_action.email


# def test_not_authenticate_action():
#     email = random_lower_string()
#     password = random_lower_string()
#     action = crud.action.authenticate(db_session, email=email, password=password)
#     assert action is None


# def test_check_if_action_is_active():
#     email = random_lower_string()
#     password = random_lower_string()
#     action_in = UserCreate(email=email, password=password)
#     action = crud.action.create(db_session, action_in=action_in)
#     is_active = crud.action.is_active(action)
#     assert is_active is True


# def test_check_if_action_is_active_inactive():
#     email = random_lower_string()
#     password = random_lower_string()
#     action_in = UserCreate(email=email, password=password, disabled=True)
#     print(action_in)
#     action = crud.action.create(db_session, action_in=action_in)
#     print(action)
#     is_active = crud.action.is_active(action)
#     print(is_active)
#     assert is_active


# def test_check_if_action_is_superaction():
#     email = random_lower_string()
#     password = random_lower_string()
#     action_in = UserCreate(email=email, password=password, is_superaction=True)
#     action = crud.action.create(db_session, action_in=action_in)
#     is_superaction = crud.action.is_superaction(action)
#     assert is_superaction is True


# def test_check_if_action_is_superaction_normal_action():
#     actionname = random_lower_string()
#     password = random_lower_string()
#     action_in = UserCreate(email=actionname, password=password)
#     action = crud.action.create(db_session, action_in=action_in)
#     is_superaction = crud.action.is_superaction(action)
#     assert is_superaction is False


# def test_get_action():
#     password = random_lower_string()
#     actionname = random_lower_string()
#     action_in = UserCreate(email=actionname, password=password, is_superaction=True)
#     action = crud.action.create(db_session, action_in=action_in)
#     action_2 = crud.action.get(db_session, action_id=action.id)
#     assert action.email == action_2.email
#     assert jsonable_encoder(action) == jsonable_encoder(action_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.actiononly
@pytest.mark.unittest
def test_create_action():
    packs_name = random_lower_string()
    packs_description = random_lower_string()
    packs_keywords = random_lower_string()
    packs_version = random_lower_string()
    packs_python_versions = random_lower_string()
    packs_author = random_lower_string()
    packs_email = "info@theblacktonystark.com"
    packs_contributors = random_lower_string()
    packs_files = random_lower_string()
    packs_path = random_lower_string()
    packs_ref = random_lower_string()

    action_name = "check_loadavg"
    action_runner_type = "remote-shell-script"
    action_description = "Check CPU Load Average on a Host"
    action_enabled = True
    action_entry_point = "checks/check_loadavg.py"
    action_parameters = {
        "period": {
            "enum": ["1", "5", "15", "all"],
            "type": "string",
            "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
            "default": "all",
            "position": 0,
        }
    }

    packs_in = PacksCreate(
        name=packs_name,
        description=packs_description,
        keywords=packs_keywords,
        version=packs_version,
        python_versions=packs_python_versions,
        author=packs_author,
        email=packs_email,
        contributors=packs_contributors,
        files=packs_files,
        path=packs_path,
        ref=packs_ref,
    )

    packs = crud.packs.create(db_session, packs_in=packs_in)

    action_in = ActionCreate(
        name=action_name,
        runner_type=action_runner_type,
        description=action_description,
        enabled=action_enabled,
        entry_point=action_entry_point,
        parameters=action_parameters,
        packs_name=packs_name,
    )

    action = crud.action.create(db_session, action_in=action_in, packs_id=packs.id)

    assert action.name == action_name
    assert action.runner_type == action_runner_type
    assert action.description == action_description
    assert action.enabled == action_enabled
    assert action.entry_point == action_entry_point
    assert action.parameters == action_parameters
    assert action.created_at == "2019-07-25 01:11:00.740428"
    assert action.updated_at == "2019-07-25 01:11:00.740428"


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.actiononly
@pytest.mark.unittest
def test_get_action():
    packs_name = random_lower_string()
    packs_description = random_lower_string()
    packs_keywords = random_lower_string()
    packs_version = random_lower_string()
    packs_python_versions = random_lower_string()
    packs_author = random_lower_string()
    packs_email = "info@theblacktonystark.com"
    packs_contributors = random_lower_string()
    packs_files = random_lower_string()
    packs_path = random_lower_string()
    packs_ref = random_lower_string()

    action_name = "check_loadavg"
    action_runner_type = "remote-shell-script"
    action_description = "Check CPU Load Average on a Host"
    action_enabled = True
    action_entry_point = "checks/check_loadavg.py"
    action_parameters = {
        "period": {
            "enum": ["1", "5", "15", "all"],
            "type": "string",
            "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
            "default": "all",
            "position": 0,
        }
    }

    packs_in = PacksCreate(
        name=packs_name,
        description=packs_description,
        keywords=packs_keywords,
        version=packs_version,
        python_versions=packs_python_versions,
        author=packs_author,
        email=packs_email,
        contributors=packs_contributors,
        files=packs_files,
        path=packs_path,
        ref=packs_ref,
    )

    packs = crud.packs.create(db_session, packs_in=packs_in)

    action_in = ActionCreate(
        name=action_name,
        runner_type=action_runner_type,
        description=action_description,
        enabled=action_enabled,
        entry_point=action_entry_point,
        parameters=action_parameters,
        packs_name=packs_name,
    )

    action = crud.action.create(db_session, action_in=action_in, packs_id=packs.id)
    action_2 = crud.action.get(db_session, action_id=action.id)
    assert jsonable_encoder(action) == jsonable_encoder(action_2)


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.actiononly
@pytest.mark.unittest
def test_update_action():
    packs_name = random_lower_string()
    packs_description = random_lower_string()
    packs_keywords = random_lower_string()
    packs_version = random_lower_string()
    packs_python_versions = random_lower_string()
    packs_author = random_lower_string()
    packs_email = "info@theblacktonystark.com"
    packs_contributors = random_lower_string()
    packs_files = random_lower_string()
    packs_path = random_lower_string()
    packs_ref = random_lower_string()

    action_name = "check_loadavg"
    action_runner_type = "remote-shell-script"
    action_description = "Check CPU Load Average on a Host"
    action_enabled = True
    action_entry_point = "checks/check_loadavg.py"
    action_parameters = {
        "period": {
            "enum": ["1", "5", "15", "all"],
            "type": "string",
            "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
            "default": "all",
            "position": 0,
        }
    }

    packs_in = PacksCreate(
        name=packs_name,
        description=packs_description,
        keywords=packs_keywords,
        version=packs_version,
        python_versions=packs_python_versions,
        author=packs_author,
        email=packs_email,
        contributors=packs_contributors,
        files=packs_files,
        path=packs_path,
        ref=packs_ref,
    )

    packs = crud.packs.create(db_session, packs_in=packs_in)

    action_in = ActionCreate(
        name=action_name,
        runner_type=action_runner_type,
        description=action_description,
        enabled=action_enabled,
        entry_point=action_entry_point,
        parameters=action_parameters,
        packs_name=packs_name,
    )

    action = crud.action.create(db_session, action_in=action_in, packs_id=packs.id)
    description2 = random_lower_string()
    action_update = ActionUpdate(description=description2)
    action2 = crud.action.update(
        db_session=db_session, action=action, action_in=action_update
    )

    assert action.name == action2.name
    assert action.runner_type == action2.runner_type
    assert action.description == description2
    assert action.enabled == action2.enabled
    assert action.entry_point == action2.entry_point
    assert action.parameters == action2.parameters
    assert action.created_at == "2019-07-25 01:11:00.740428"
    assert action.updated_at == "2019-07-25 01:11:00.740428"


@freeze_time("2019-07-25 01:11:00.740428")
@pytest.mark.actiononly
@pytest.mark.unittest
def test_delete_action():
    packs_name = random_lower_string()
    packs_description = random_lower_string()
    packs_keywords = random_lower_string()
    packs_version = random_lower_string()
    packs_python_versions = random_lower_string()
    packs_author = random_lower_string()
    packs_email = "info@theblacktonystark.com"
    packs_contributors = random_lower_string()
    packs_files = random_lower_string()
    packs_path = random_lower_string()
    packs_ref = random_lower_string()

    action_name = "check_loadavg"
    action_runner_type = "remote-shell-script"
    action_description = "Check CPU Load Average on a Host"
    action_enabled = True
    action_entry_point = "checks/check_loadavg.py"
    action_parameters = {
        "period": {
            "enum": ["1", "5", "15", "all"],
            "type": "string",
            "description": "Time period for load avg: 1,5,15 minutes, or 'all'",
            "default": "all",
            "position": 0,
        }
    }

    packs_in = PacksCreate(
        name=packs_name,
        description=packs_description,
        keywords=packs_keywords,
        version=packs_version,
        python_versions=packs_python_versions,
        author=packs_author,
        email=packs_email,
        contributors=packs_contributors,
        files=packs_files,
        path=packs_path,
        ref=packs_ref,
    )

    packs = crud.packs.create(db_session, packs_in=packs_in)

    action_in = ActionCreate(
        name=action_name,
        runner_type=action_runner_type,
        description=action_description,
        enabled=action_enabled,
        entry_point=action_entry_point,
        parameters=action_parameters,
        packs_name=packs_name,
    )

    action = crud.action.create(db_session, action_in=action_in, packs_id=packs.id)

    action2 = crud.action.remove(db_session=db_session, action_id=action.id)

    action3 = crud.action.get(db_session=db_session, action_id=action.id)

    assert action3 is None

    assert action2.id == action.id
    assert action2.name == action_name
    assert action2.runner_type == action_runner_type
    assert action2.description == action_description
    assert action2.enabled == action_enabled
    assert action2.entry_point == action_entry_point
    assert action2.parameters == action_parameters
    assert action2.created_at == "2019-07-25 01:11:00.740428"
    assert action2.updated_at == "2019-07-25 01:11:00.740428"
