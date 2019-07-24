# from fastapi.encoders import jsonable_encoder

# from tests.utils.utils import random_lower_string
# from ultron8.api import crud
# from ultron8.api.db.u_sqlite.session import db_session
# from ultron8.api.models.action import RunnerTypeModel
# from ultron8.api.models.action import ActionBase
# from ultron8.api.models.action import ActionBaseInDB
# from ultron8.api.models.action import ActionCreate
# from ultron8.api.models.action import ActionUpdate


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
