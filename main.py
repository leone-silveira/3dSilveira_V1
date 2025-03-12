from fastapi import FastAPI
from routers import filaments

app = FastAPI(
    title="Filament API",
    description="API for 3d filaments purpose. Analysis for minor cost",
    version="1.0.0"
)

app.include_router(filaments.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "You're online ! "}
