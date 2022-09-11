from fastapi import FastAPI

from app.api.router import api_router
from app.database.database import engine
from app.models import metadata

app = FastAPI(title="Hello!")


@app.on_event("startup")
async def startup_event():
    metadata.bind = engine


app.include_router(api_router, prefix="/api")


@app.on_event("shutdown")
def shutdown_event():
    pass
