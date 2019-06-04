from ultron8.api.db.u_sqlite import (
    open_database_connection_pool,
    close_database_connection_pool,
)
from ultron8.api import settings
from fastapi import Depends, FastAPI, Header, HTTPException

from ultron8.api.routers import items, users, home, version, guid


# SOURCE: https://github.com/nwcell/guid_tracker/blob/aef948336ba268aa06df7cc9e7e6768b08d0f363/src/guid/main.py
app = FastAPI(title="Ultron-8 Web Server")

app.debug = settings.DEBUG

app.add_event_handler("startup", open_database_connection_pool)
app.add_event_handler("shutdown", close_database_connection_pool)

# app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(home.router)
app.include_router(version.router)
app.include_router(users.router)
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(guid.router, prefix="/guid", tags=["guid"])

# NOTE: from guid tracker
# app.include_router(api_router)
