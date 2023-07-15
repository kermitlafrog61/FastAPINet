import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from apps.posts.routers import router as posts_router
from apps.users.routers import router as users_router

from core.db import Base


app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)


if __name__ == "__main__":
    Base.metadata.create_all()
    uvicorn.run(app, host="0000000", port=8000)
