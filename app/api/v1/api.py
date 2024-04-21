from fastapi import APIRouter

from app.api.v1.endpoints import influencer

api_router = APIRouter()

api_router.include_router(influencer.router, prefix="/influencer", tags=["influencer"])