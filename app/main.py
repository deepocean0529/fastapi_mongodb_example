from contextlib import asynccontextmanager
from typing import List

from fastapi import Body, Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import dbm
from app.resources import secrets
from app.resources.logger import logger
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    dbm.connect_to_database()
    yield
    dbm.close_database_connection()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path.startswith("/api"):

        try:
            authorization: str = request.headers.get("Authorization")

            logger.info(f"auth_middleware: {authorization}")

            if not authorization:
                raise Exception("Not Authorized")

            scheme, _, token = authorization.partition(" ")
            if scheme.lower() != "bearer":
                raise Exception("Not Authorized")

            if token != secrets.API_KEY:
                raise Exception("Not Authorized")
        except Exception as e:
            logger.error(f"Auth Middleware Error: {e}")
            return JSONResponse("Not Authorized", status.HTTP_401_UNAUTHORIZED)

    return await call_next(request)


@app.get("/")
def hello():
    return "Hello!"


app.include_router(api_router, prefix="/api/v1")