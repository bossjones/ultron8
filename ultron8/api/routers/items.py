"""Temporary router for user objects. Taken directly from FastApi Tutorial"""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/v1/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@router.put(
    "/v1/items/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
def update_item(item_id: str):
    if item_id != "foo":
        raise HTTPException(status_code=403, detail="You can only update the item: foo")
    return {"item_id": item_id, "name": "The Fighters"}
