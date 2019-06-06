from ultron8.api.db.u_sqlite import (
    open_database_connection_pool,
    close_database_connection_pool,
)
from ultron8.api import settings
from fastapi import Depends, FastAPI, Header, HTTPException

from ultron8.api.routers import items, users, home, version, guid, alive
from ultron8.api.middleware.logging import log
from starlette.staticfiles import StaticFiles
from pathlib import Path
from starlette.responses import PlainTextResponse, RedirectResponse, UJSONResponse
from starlette.middleware.cors import CORSMiddleware
import starlette_prometheus
import logging
from starlette.requests import Request

from ultron8.api.db.u_sqlite.session import Session

logger = logging.getLogger(__name__)

# TODO: As soon as we merge web.py into the MCP, we will want to nuke this setup_logging line!!!
log.setup_logging()

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

app.debug = settings.DEBUG
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_CORS_ORIGINS],
    allow_methods=[settings.BACKEND_CORS_ORIGINS],
    allow_headers=[settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
)

app.add_middleware(starlette_prometheus.PrometheusMiddleware)

app.add_event_handler("startup", open_database_connection_pool)
app.add_event_handler("shutdown", close_database_connection_pool)

# app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.add_route("/metrics/", starlette_prometheus.metrics)

app.include_router(home.router)
app.include_router(alive.router, tags=["alive"])
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
