from ultron8.api.db.u_sqlite import (
    open_database_connection_pool,
    close_database_connection_pool,
)
from ultron8.api import settings
from fastapi import Depends, FastAPI, Header, HTTPException

from ultron8.api.routers import items, users, home, version, guid, alive
from starlette.staticfiles import StaticFiles
from pathlib import Path
from starlette.responses import PlainTextResponse, RedirectResponse, UJSONResponse
from starlette.middleware.cors import CORSMiddleware
import starlette_prometheus
import logging

logger = logging.getLogger(__name__)

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
)

app.add_middleware(PrometheusMiddleware)

app.add_event_handler("startup", open_database_connection_pool)
app.add_event_handler("shutdown", close_database_connection_pool)

# app = FastAPI()


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.add_route("/metrics/", metrics)

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
