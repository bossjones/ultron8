"""Dev version of web.py, allows us to keep ipython inside of here and jump down into pdb when stuff breaks/happens"""

import sys

# import better_exceptions; better_exceptions.hook()

# from IPython.core.debugger import Tracer  # noqa
# from IPython.core import ultratb

# sys.excepthook = ultratb.FormattedTB(
#     mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
# )


import logging
from pathlib import Path

import starlette_prometheus
import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.responses import RedirectResponse
from starlette.responses import UJSONResponse
from starlette.staticfiles import StaticFiles

from ultron8.api import settings
from ultron8.api.api_v1.endpoints import alive
from ultron8.api.api_v1.endpoints import guid
from ultron8.api.api_v1.endpoints import home
from ultron8.api.api_v1.endpoints import items
from ultron8.api.api_v1.endpoints import login
from ultron8.api.api_v1.endpoints import token
from ultron8.api.api_v1.endpoints import users
from ultron8.api.api_v1.endpoints import version
from ultron8.api.db.u_sqlite import close_database_connection_pool
from ultron8.api.db.u_sqlite import open_database_connection_pool
from ultron8.api.db.u_sqlite.session import Session
from ultron8.api.middleware.logging import log

# from ultron8.api.routers import items, users, home, version, guid, alive


# TODO: As soon as we merge web.py into the MCP, we will want to nuke this setup_logging line!!!
log.setup_logging()

LOGGER = logging.getLogger(__name__)

LOGGER.setLevel(settings.LOG_LEVEL)

# # NOTE: If debug logging is enabled, then turn on debug logging for everything in app
# if settings.LOG_LEVEL == logging.DEBUG:

#     # Enable connection pool logging
#     # SOURCE: https://docs.sqlalchemy.org/en/13/core/engines.html#dbengine-logging
#     SQLALCHEMY_POOL_LOGGER = logging.getLogger("sqlalchemy.pool")
#     SQLALCHEMY_ENGINE_LOGGER = logging.getLogger("sqlalchemy.engine")
#     SQLALCHEMY_ORM_LOGGER = logging.getLogger("sqlalchemy.orm")
#     SQLALCHEMY_DIALECTS_LOGGER = logging.getLogger("sqlalchemy.dialects")
#     UVICORN_LOGGER = logging.getLogger("uvicorn")
#     SQLALCHEMY_POOL_LOGGER.setLevel(logging.DEBUG)
#     SQLALCHEMY_ENGINE_LOGGER.setLevel(logging.DEBUG)
#     SQLALCHEMY_ORM_LOGGER.setLevel(logging.DEBUG)
#     SQLALCHEMY_DIALECTS_LOGGER.setLevel(logging.DEBUG)
#     UVICORN_LOGGER.setLevel(logging.DEBUG)

# if settings.DEBUG_REQUESTS:
#     # import requests.packages.urllib3.connectionpool as http_client
#     # http_client.HTTPConnection.debuglevel = 1
#     REQUESTS_LOGGER = logging.getLogger("requests")
#     REQUESTS_LOGGER.setLevel(logging.DEBUG)
#     REQUESTS_LOGGER.propagate = True
#     URLLIB3_LOGGER = logging.getLogger("urllib3")
#     URLLIB3_LOGGER.setLevel(logging.DEBUG)

# SOURCE: https://github.com/nwcell/guid_tracker/blob/aef948336ba268aa06df7cc9e7e6768b08d0f363/src/guid/main.py
app = FastAPI(title="Ultron-8 Web Server")

LOGGER.info(f" [DEBUG] {settings.DEBUG}")

app.debug = settings.DEBUG
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static",
)

# CORS
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=[settings.BACKEND_CORS_ORIGINS],
    allow_headers=[settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
)

app.add_middleware(starlette_prometheus.PrometheusMiddleware)

app.add_route(f"{settings.API_V1_STR}/metrics", starlette_prometheus.metrics)

app.include_router(token.router, tags=["token"], prefix=f"{settings.API_V1_STR}")
app.include_router(home.router, tags=["home"], prefix=f"{settings.API_V1_STR}")
app.include_router(alive.router, tags=["alive"], prefix=f"{settings.API_V1_STR}")
app.include_router(version.router, tags=["version"], prefix=f"{settings.API_V1_STR}")
app.include_router(login.router, tags=["login"], prefix=f"{settings.API_V1_STR}")
app.include_router(users.router, tags=["users"], prefix=f"{settings.API_V1_STR}/users")
app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


if __name__ == "__main__":
    import os

    # HOST = os.environ.get("HOST", "localhost")
    HOST = "localhost"
    PORT = int(os.environ.get("PORT", 11267))
    print(f" [HOST] {HOST}")
    print(f" [PORT] {PORT}")
    uvicorn.run(
        app, host=HOST, port=PORT, logger=LOGGER, log_level=settings._USER_LOG_LEVEL
    )
