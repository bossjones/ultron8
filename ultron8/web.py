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
from ultron8.api.api_v1.endpoints import loggers as log_endpoint
from ultron8.api.db.u_sqlite import close_database_connection_pool
from ultron8.api.db.u_sqlite import open_database_connection_pool
from ultron8.api.db.u_sqlite.session import Session
from ultron8.api.middleware.logging import log

# from ultron8.api.routers import items, users, home, version, guid, alive

logger = logging.getLogger(__name__)

# TODO: As soon as we merge web.py into the MCP, we will want to nuke this setup_logging line!!!
log.setup_logging()


# # Suppress overly verbose logs from libraries that aren't helpful
# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.getLogger('urllib3').setLevel(logging.WARNING)
# logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

# ---------------------------------------------------------------------
# SOURCE: https://github.com/webrecorder/browsertrix/blob/f6152b780e054940fbd2d336869ebf0fa052147d/browsertrix/crawl.py
# from asyncio import AbstractEventLoop, gather as aio_gather, get_event_loop


# async def startup(self) -> None:
#     """Initialize the crawler manager's redis connection and
#     http session used to make requests to shepherd
#     """
#     self.loop = get_event_loop()
#     self.redis = await init_redis(
#         env('REDIS_URL', default=DEFAULT_REDIS_URL), self.loop
#     )
#     self.session = ClientSession(
#         connector=TCPConnector(
#             resolver=AsyncResolver(loop=self.loop), loop=self.loop
#         ),
#         json_serialize=partial(json.dumps, ensure_ascii=False),
#         loop=self.loop,
#     )

# async def shutdown(self) -> None:
#     """Closes the redis connection and http session"""
#     try:
#         self.redis.close()
#         await self.redis.wait_closed()
#     except Exception:
#         pass

#     try:
#         await self.session.close()
#     except Exception:
#         pass
# ---------------------------------------------------------------------

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc) -> Any:
#     logging.getLogger(__name__).exception(f"{request.method} {request.url} {exc}")
#     return await http_exception_handler(request, exc)


# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc) -> Any:
#     logging.getLogger(__name__).exception(f"{request.method} {request.url} {exc}")
#     return await request_validation_exception_handler(request, exc)

# SOURCE: https://github.com/nwcell/guid_tracker/blob/aef948336ba268aa06df7cc9e7e6768b08d0f363/src/guid/main.py
app = FastAPI(title="Ultron-8 Web Server")

logger.info(f" settings.DEBUG={settings.DEBUG}")

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


# -----------------------------------------------------------------------
# DISABLED: originally from guid_tracker
# -----------------------------------------------------------------------
# app.add_event_handler("startup", open_database_connection_pool)
# app.add_event_handler("shutdown", close_database_connection_pool)
# -----------------------------------------------------------------------

# app = FastAPI()


# async def get_token_header(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")


app.add_route(f"{settings.API_V1_STR}/metrics", starlette_prometheus.metrics)

app.include_router(log_endpoint.router, tags=["log"], prefix=f"{settings.API_V1_STR}")
app.include_router(token.router, tags=["token"], prefix=f"{settings.API_V1_STR}")
app.include_router(home.router, tags=["home"], prefix=f"{settings.API_V1_STR}")
app.include_router(alive.router, tags=["alive"], prefix=f"{settings.API_V1_STR}")
app.include_router(version.router, tags=["version"], prefix=f"{settings.API_V1_STR}")
app.include_router(login.router, tags=["login"], prefix=f"{settings.API_V1_STR}")
app.include_router(users.router, tags=["users"], prefix=f"{settings.API_V1_STR}/users")
app.include_router(
    items.router,
    prefix=f"{settings.API_V1_STR}/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)

# app.include_router(guid.router, prefix="/guid", tags=["guid"])


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


# NOTE: from guid tracker


# FIXME: Enable this
# def creates_web_app():
#     """Create the fastapi web application
#     Returns:
#         [fastapi.FastAPI]: the main application
#     """

#     logger.info(f"Create fastapi web application ...")


#     app = FastAPI(title="Ultron-8 Web Server")
#     app.debug = settings.DEBUG
#     app.mount(
#         "/static",
#         StaticFiles(directory=str(Path(__file__).parent / "static")),
#         name="static",
#     )

#     app.add_middleware(
#         CORSMiddleware, allow_origins=[settings.BACKEND_CORS_ORIGINS], allow_methods=[settings.BACKEND_CORS_ORIGINS], allow_headers=[settings.BACKEND_CORS_ORIGINS]
#     )
#     app.add_middleware(starlette_prometheus.PrometheusMiddleware)

#     app.add_event_handler("startup", open_database_connection_pool)
#     app.add_event_handler("shutdown", close_database_connection_pool)


#     app.add_route("/metrics/", starlette_prometheus.metrics)

#     app.include_router(home.router)
#     app.include_router(alive.router, tags=["alive"])
#     app.include_router(version.router)
#     app.include_router(users.router)
#     app.include_router(
#         items.router,
#         prefix="/items",
#         tags=["items"],
#         dependencies=[Depends(get_token_header)],
#         responses={404: {"description": "Not found"}},
#     )

#     app.include_router(guid.router, prefix="/guid", tags=["guid"])
#     return app

# app = creates_web_app()
if __name__ == "__main__":
    import os

    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = os.environ.get("PORT", 11267)
    # uvicorn.run(app, host=HOST, port=PORT)

    # uvicorn.run(app, host=HOST, port=PORT, log_level=settings._USER_LOG_LEVEL.lower(), reload=True, workers=settings.WORKERS)
    # uvicorn.run(app, host=HOST, port=PORT, log_level=settings._USER_LOG_LEVEL.lower(), reload=True)
    APP_MODULE_STR = os.environ.get("APP_MODULE")
    app_import_str = f"{APP_MODULE_STR}"
    uvicorn.run(
        app_import_str,
        host=HOST,
        port=PORT,
        log_level=settings._USER_LOG_LEVEL.lower(),
        reload=True,
    )
