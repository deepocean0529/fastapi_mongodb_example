from bson import ObjectId, json_util
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response, status
from fastapi.security import HTTPBearer
from pymongo import ReturnDocument

from app.utils import oid_json_parse
from app.db import dbm
from app.models.Influencer import TABLE_NAME_INFLUENCER, Influencer, Influencer_Update
from app.resources.logger import logger

router = APIRouter()


@router.get(
    "/",
    response_description="List all influencers",
    dependencies=[Depends(HTTPBearer())],
)
async def get_influencer_list(request: Request, limit: int = 100):
    """
    [influencers]データベースからリストを取得する
    """
    list = dbm.db[TABLE_NAME_INFLUENCER].find({}).limit(limit=limit)
    return oid_json_parse(list)


@router.get(
    "/{id}",
    response_description="Get influencer by id",
    dependencies=[Depends(HTTPBearer())],
)
async def get_influencer(id: str, request: Request):
    """
    指定のインフルエンサー情報を返却する
    """

    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{id} is not valid id format.",
        )

    influencer = dbm.db[TABLE_NAME_INFLUENCER].find_one({"_id": objId})

    if influencer is not None:
        return oid_json_parse(influencer)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Influencer with ID {id} not found",
    )


@router.post(
    "/",
    response_description="Create a new influencer",
    dependencies=[Depends(HTTPBearer())],
)
async def create_influencer(request: Request, influencer: Influencer = Body(...)):
    """
    新規インフルエンサーを登録する
    """
    new_influencer = dbm.db[TABLE_NAME_INFLUENCER].insert_one(
        influencer.model_dump(by_alias=True, exclude=["id"])
    )

    created_influencer = dbm.db[TABLE_NAME_INFLUENCER].find_one(
        {"_id": new_influencer.inserted_id}
    )
    return oid_json_parse(created_influencer)


@router.put(
    "/{id}",
    response_description="Update an influencer",
    dependencies=[Depends(HTTPBearer())],
)
async def update_influencer(
    id: str, request: Request, influencer: Influencer_Update = Body(...)
):
    """
    インフルエンサーの登録情報を更新する。

    指定の項目のみ更新される。未指定の項目は変更しない。
    """
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{id} is not valid id format.",
        )

    influencer = {
        k: v
        for k, v in influencer.model_dump(by_alias=True, exclude=["id"]).items()
        if v is not None
    }

    if len(influencer) >= 1:
        update_result = dbm.db[TABLE_NAME_INFLUENCER].find_one_and_update(
            {"_id": objId},
            {"$set": influencer},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return oid_json_parse(update_result)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"influencer {id} not found",
            )

    # The update is empty, but we should still return the matching document:
    if (
        existing_influencer := await dbm.db[TABLE_NAME_INFLUENCER].find_one({"_id": id})
    ) is not None:
        return oid_json_parse(existing_influencer)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Influencer {id} not found"
    )


@router.delete(
    "/{id}",
    response_description="Delete an influencer",
    dependencies=[Depends(HTTPBearer())],
)
async def delete_influencer(id: str, request: Request):
    """
    指定のインフルエンサーを削除する。
    """
    try:
        objId = ObjectId(id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{id} is not valid id format.",
        )

    delete_result = dbm.db[TABLE_NAME_INFLUENCER].delete_one({"_id": objId})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Influencer {id} not found"
    )
