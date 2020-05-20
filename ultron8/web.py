# NOTE: Uncomment to enabled debugger in vscode # try:
# NOTE: Uncomment to enabled debugger in vscode #     import ptvsd
# NOTE: Uncomment to enabled debugger in vscode # except Exception:
# NOTE: Uncomment to enabled debugger in vscode #     print("WARNING - ptvsd is not installed, can't use to debug in vscode")
# NOTE: Uncomment to enabled debugger in vscode #     pass

import os

# NOTE: Uncomment to enabled debugger in vscode #     # SOURCE: https://github.com/microsoft/ptvsd/blob/master/TROUBLESHOOTING.md#1-multiprocessing-on-linuxmac
# NOTE: Uncomment to enabled debugger in vscode #     # Multiprocess debugging on a Linux machine requires the spawn setting. We are working on improving this experience, see # NOTE: Uncomment to enabled debugger in vscode #943. Meanwhile do this to improve your debugging experience:
# NOTE: Uncomment to enabled debugger in vscode # if os.getenv("ULTRON_ENVIRONMENT", "production") == "development":
# NOTE: Uncomment to enabled debugger in vscode #     # See: https://github.com/microsoft/ptvsd/issues/1056
# NOTE: Uncomment to enabled debugger in vscode #     # multiprocess debugging requires spawn method
# NOTE: Uncomment to enabled debugger in vscode #     # @ref: https://github.com/microsoft/ptvsd/blob/master/TROUBLESHOOTING.md#1-multiprocessing-on-linuxmac
# NOTE: Uncomment to enabled debugger in vscode #     import multiprocessing
# NOTE: Uncomment to enabled debugger in vscode
# NOTE: Uncomment to enabled debugger in vscode #     multiprocessing.set_start_method("spawn", True)

import subprocess

# SOURCE: https://blog.hipolabs.com/remote-debugging-with-vscode-docker-and-pico-fde11f0e5f1c
def start_debugger():
    parent_pid = os.getppid()
    # cmd = "ps aux | grep %s | awk '{print $2}'" % "ULTRON_ENABLE_WEB"
    cmd = "ps aux | grep 'python ultron8/web.py' | awk '{print $2}' | head -1"
    ps = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=4096,
        shell=True,
        universal_newlines=True,
    )

    output, _ = ps.communicate()
    pids = output.split("\n")
    # using list comprehension to perform removal of empty strings
    pids = [i for i in pids if i]
    return parent_pid, pids


# NOTE: Uncomment to enabled debugger in vscode # if os.getenv("ULTRON_ENVIRONMENT", "production") == "development":
# NOTE: Uncomment to enabled debugger in vscode
# NOTE: Uncomment to enabled debugger in vscode #     # SOURCE: https://github.com/microsoft/ptvsd/blob/master/TROUBLESHOOTING.md#1-multiprocessing-on-linuxmac
# NOTE: Uncomment to enabled debugger in vscode #     # Multiprocess debugging on a Linux machine requires the spawn setting. We are working on improving this experience, see # NOTE: Uncomment to enabled debugger in vscode #943. Meanwhile do this to improve your debugging experience:
# NOTE: Uncomment to enabled debugger in vscode #     parent_pid, pids = start_debugger()
# NOTE: Uncomment to enabled debugger in vscode #     print(f" [parent_pid] {parent_pid}")
# NOTE: Uncomment to enabled debugger in vscode #     print(f" [pids] {pids}")
# NOTE: Uncomment to enabled debugger in vscode #     if str(parent_pid) in pids:
# NOTE: Uncomment to enabled debugger in vscode #         print("Starting debugger")
# NOTE: Uncomment to enabled debugger in vscode #         try:
# NOTE: Uncomment to enabled debugger in vscode #             ptvsd.enable_attach()
# NOTE: Uncomment to enabled debugger in vscode #         except Exception:
# NOTE: Uncomment to enabled debugger in vscode #             print("WARNING - ptvsd is not installed, can't run ptvsd.enable_attach()")
# NOTE: Uncomment to enabled debugger in vscode #             pass


import logging
from pathlib import Path

import time

import starlette_prometheus
import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Header
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.responses import RedirectResponse
from starlette.responses import UJSONResponse
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import JSONResponse


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

# import sys
# from IPython.core.debugger import Tracer  # noqa
# from IPython.core import ultratb

# sys.excepthook = ultratb.FormattedTB(
#     mode="Verbose", color_scheme="Linux", call_pdb=True, ostream=sys.__stdout__
# )

##########################################################################
# # FIXME: #46 5/18/2020 Stop using the setup_logging function and use the one defined in "from ultron8.api.middleware.logging import log"
# from ultron8.api.applog import read_logging_config, setup_logging

# logconfig_dict = read_logging_config("logging.yml")

# setup_logging(logconfig_dict)

# LOGGER = logging.getLogger(__name__)

# LOGGER.setLevel(settings.LOG_LEVEL)
##########################################################################

# from ultron8.api.routers import items, users, home, version, guid, alive

logger = logging.getLogger(__name__)

# TODO: As soon as we merge web.py into the MCP, we will want to nuke this setup_logging line!!!
log.setup_logging()


# NOTE: If debug logging is enabled, then turn on debug logging for everything in app
if settings.LOG_LEVEL == logging.DEBUG:

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
    #    UVICORN_LOGGER.setLevel(logging.DEBUG)
    FASTAPI_LOGGER = logging.getLogger("fastapi")
    FASTAPI_LOGGER.setLevel(logging.DEBUG)


# if settings.DEBUG_REQUESTS:
#     # import requests.packages.urllib3.connectionpool as http_client
#     # http_client.HTTPConnection.debuglevel = 1
#     REQUESTS_LOGGER = logging.getLogger("requests")
#     REQUESTS_LOGGER.setLevel(logging.DEBUG)
#     REQUESTS_LOGGER.propagate = True
#     URLLIB3_LOGGER = logging.getLogger("urllib3")
#     URLLIB3_LOGGER.setLevel(logging.DEBUG)

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


# # SOURCE: https://fastapi.tiangolo.com/tutorial/sql-databases/#main-fastapi-app
# # Dependency
# def get_db():
#     try:
#         db = Session()
#         yield db
#     finally:
#         db.close()

# NOTE: Async version
# DISABLED: # # SOURCE: https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body
# DISABLED: # @app.exception_handler(RequestValidationError)
# DISABLED: # async def validation_exception_handler(request: Request, exc: RequestValidationError):
# DISABLED: #     print(jsonable_encoder({"detail": exc.errors(), "body": exc.body}))
# DISABLED: #     return JSONResponse(
# DISABLED: #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
# DISABLED: #         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
# DISABLED: #     )


# @app.exception_handler(RequestValidationError)
# SOURCE: https://fastapi.tiangolo.com/tutorial/handling-errors/#use-the-requestvalidationerror-body
def validation_exception_handler(request: Request, exc: RequestValidationError):
    # print(jsonable_encoder({"detail": exc.errors(), "body": exc.body}))
    print(f"OMG! The client sent invalid data!: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# def misc_exception_handler(request: Request, exc: Exception):
#     logger.exception(exc)
#     return JSONResponse('Unexpected error', status_code=500)


# async def log_request(request, call_next):
#     logger.info(f'{request.method} {request.url}')
#     response = await call_next(request)
#     logger.info(f'Status code: {response.status_code}')
#     body = b""
#     async for chunk in response.body_iterator:
#         body += chunk
#     # do something with body ...
#     logger.info("[body]: ")
#     logger.info(body)

#     return Response(
#         content=body,
#         status_code=response.status_code,
#         headers=dict(response.headers),
#         media_type=response.media_type
#     )

# SOURCE: https://stackoverflow.com/questions/60778279/fastapi-middleware-peeking-into-responses
class LogRequestMiddleware(BaseHTTPMiddleware):
    """Alternate implementation for:

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        # NOTE: request.state is a property of each Request object. It is there to store arbitrary objects attached to the request itself, like the database session in this case. You can read more about it in Starlette's docs about Request state.
        # For us in this case, it helps us ensure a single database session is used through all the request, and then closed afterwards (in the middleware).
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = Session()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    Arguments:
        BaseHTTPMiddleware {[type]} -- [description]
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        logger.info(f"{request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Status code: {response.status_code}")
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        # do something with body ...
        logger.info("[body]: ")
        logger.info(body)
        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )


def get_application() -> FastAPI:
    # SOURCE: https://github.com/nwcell/guid_tracker/blob/aef948336ba268aa06df7cc9e7e6768b08d0f363/src/guid/main.py
    app = FastAPI(title="Ultron-8 Web Server")

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    # app.add_exception_handler(Exception, misc_exception_handler)

    logger.info(f"Create fastapi web application ...")

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

    app.include_router(
        log_endpoint.router, tags=["log"], prefix=f"{settings.API_V1_STR}/logs"
    )
    app.include_router(token.router, tags=["token"], prefix=f"{settings.API_V1_STR}")
    app.include_router(home.router, tags=["home"], prefix=f"{settings.API_V1_STR}")
    app.include_router(alive.router, tags=["alive"], prefix=f"{settings.API_V1_STR}")
    app.include_router(
        version.router, tags=["version"], prefix=f"{settings.API_V1_STR}"
    )
    app.include_router(login.router, tags=["login"], prefix=f"{settings.API_V1_STR}")
    app.include_router(
        users.router, tags=["users"], prefix=f"{settings.API_V1_STR}/users"
    )
    app.include_router(
        items.router,
        prefix=f"{settings.API_V1_STR}/items",
        tags=["items"],
        # dependencies=[Depends(get_token_header)],
        # responses={404: {"description": "Not found"}},
    )

    # # app.include_router(guid.router, prefix="/guid", tags=["guid"])

    # # SOURCE: https://fastapi.tiangolo.com/tutorial/sql-databases/#alternative-db-session-with-middleware
    # # to we make sure the database session is always closed after the request. Even if there was an exception while processing the request.
    # @app.middleware("http")
    # async def db_session_middleware(request: Request, call_next):
    #     """The middleware we'll add (just a function) will create a new SQLAlchemy SessionLocal for each request, add it to the request and then close it once the request is finished.

    #     Arguments:
    #         request {Request} -- [description]
    #         call_next {[type]} -- [description]

    #     Returns:
    #         [type] -- FastAPI Response
    #     """
    #     # NOTE: request.state is a property of each Request object. It is there to store arbitrary objects attached to the request itself, like the database session in this case. You can read more about it in Starlette's docs about Request state.
    #     # For us in this case, it helps us ensure a single database session is used through all the request, and then closed afterwards (in the middleware).
    #     response = Response("Internal server error", status_code=500)
    #     try:
    #         request.state.db = Session()
    #         response = await call_next(request)
    #     finally:
    #         request.state.db.close()
    #     return response
    app.add_middleware(DbSessionMiddleware)

    # only add this logging middleware if we have this in super debug mode ( since it is noisey )
    if os.getenv("ULTRON_ENVIRONMENT", "production") == "development":
        app.add_middleware(LogRequestMiddleware)

    return app


# SOURCE: https://fastapi.tiangolo.com/tutorial/sql-databases/#alternative-db-session-with-middleware
# to we make sure the database session is always closed after the request. Even if there was an exception while processing the request.
# SOURCE: https://www.starlette.io/middleware/
class DbSessionMiddleware(BaseHTTPMiddleware):
    """Alternate implementation for:

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        # NOTE: request.state is a property of each Request object. It is there to store arbitrary objects attached to the request itself, like the database session in this case. You can read more about it in Starlette's docs about Request state.
        # For us in this case, it helps us ensure a single database session is used through all the request, and then closed afterwards (in the middleware).
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = Session()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    Arguments:
        BaseHTTPMiddleware {[type]} -- [description]
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = Session()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response


class AddProcessTimeMiddleware(BaseHTTPMiddleware):
    """Figure out how long it takes for a request to process.

    Arguments:
        BaseHTTPMiddleware {[type]} -- [description]
    """

    # SOURCE: https://github.com/podhmo/individual-sandbox/blob/c666a27f8bacb8a56750c74998d80405b92cb4e8/daily/20191220/example_starlette/04fastapi-jinja2-with-middleware/test_main.py
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


# # SOURCE: https://github.com/nwcell/guid_tracker/blob/aef948336ba268aa06df7cc9e7e6768b08d0f363/src/guid/main.py
# app = FastAPI(title="Ultron-8 Web Server")

# logger.info(f" settings.DEBUG={settings.DEBUG}")

# app.debug = settings.DEBUG
# app.mount(
#     "/static",
#     StaticFiles(directory=str(Path(__file__).parent / "static")),
#     name="static",
# )

# # CORS
# origins = []

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_methods=[settings.BACKEND_CORS_ORIGINS],
#     allow_headers=[settings.BACKEND_CORS_ORIGINS],
#     allow_credentials=True,
# )

# app.add_middleware(starlette_prometheus.PrometheusMiddleware)


# # -----------------------------------------------------------------------
# # DISABLED: originally from guid_tracker
# # -----------------------------------------------------------------------
# # app.add_event_handler("startup", open_database_connection_pool)
# # app.add_event_handler("shutdown", close_database_connection_pool)
# # -----------------------------------------------------------------------

# # app = FastAPI()


# # async def get_token_header(x_token: str = Header(...)):
# #     if x_token != "fake-super-secret-token":
# #         raise HTTPException(status_code=400, detail="X-Token header invalid")


# app.add_route(f"{settings.API_V1_STR}/metrics", starlette_prometheus.metrics)

# app.include_router(
#     log_endpoint.router, tags=["log"], prefix=f"{settings.API_V1_STR}/logs"
# )
# app.include_router(token.router, tags=["token"], prefix=f"{settings.API_V1_STR}")
# app.include_router(home.router, tags=["home"], prefix=f"{settings.API_V1_STR}")
# app.include_router(alive.router, tags=["alive"], prefix=f"{settings.API_V1_STR}")
# app.include_router(version.router, tags=["version"], prefix=f"{settings.API_V1_STR}")
# app.include_router(login.router, tags=["login"], prefix=f"{settings.API_V1_STR}")
# app.include_router(users.router, tags=["users"], prefix=f"{settings.API_V1_STR}/users")
# app.include_router(
#     items.router,
#     prefix=f"{settings.API_V1_STR}/items",
#     tags=["items"],
#     # dependencies=[Depends(get_token_header)],
#     # responses={404: {"description": "Not found"}},
# )

# # app.include_router(guid.router, prefix="/guid", tags=["guid"])


# # # SOURCE: https://fastapi.tiangolo.com/tutorial/sql-databases/#alternative-db-session-with-middleware
# # # to we make sure the database session is always closed after the request. Even if there was an exception while processing the request.
# # @app.middleware("http")
# # async def db_session_middleware(request: Request, call_next):
# #     """The middleware we'll add (just a function) will create a new SQLAlchemy SessionLocal for each request, add it to the request and then close it once the request is finished.

# #     Arguments:
# #         request {Request} -- [description]
# #         call_next {[type]} -- [description]

# #     Returns:
# #         [type] -- FastAPI Response
# #     """
# #     # NOTE: request.state is a property of each Request object. It is there to store arbitrary objects attached to the request itself, like the database session in this case. You can read more about it in Starlette's docs about Request state.
# #     # For us in this case, it helps us ensure a single database session is used through all the request, and then closed afterwards (in the middleware).
# #     response = Response("Internal server error", status_code=500)
# #     try:
# #         request.state.db = Session()
# #         response = await call_next(request)
# #     finally:
# #         request.state.db.close()
# #     return response


# app.add_middleware(DbSessionMiddleware)

# # NOTE: from guid tracker


app = get_application()

print(" [app] ran get_application")

if __name__ == "__main__":
    # import os
    HOST = "localhost"
    PORT = int(os.environ.get("PORT", 11267))

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
