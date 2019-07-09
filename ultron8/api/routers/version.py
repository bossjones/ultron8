# """Temporary router for user objects. Taken directly from FastApi Tutorial"""
# from starlette.responses import UJSONResponse
# from ultron8 import __version__
# from fastapi import APIRouter, HTTPException
# from ultron8.api.models.version import VersionOut
# router = APIRouter()
# @router.get("/version", tags=["version"], response_model=VersionOut)
# async def read_version():
#     cur_version = f"{__version__}"
#     content = {"version": cur_version}
#     # content_out = UJSONResponse(content)
#     return VersionOut(**content)
