from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ultron8.api import crud, settings
from ultron8.api.core.jwt import create_access_token
from ultron8.api.core.security import get_password_hash
from ultron8.api.models.token import Token
from ultron8.api.utils.db import get_db

# import crud
# from api.utils.db import get_db
# from core import settings
# from core.jwt import create_access_token
# from core.security import get_password_hash
# from models.user import User as DBUSER
# from schema.token import Token


router = APIRouter()


@router.post("/token", response_model=Token, tags=["token"])
def get_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Account Deactivated")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
