from fastapi import FastAPI
import uvicorn
from routers import filaments

app = FastAPI(
    title="Filament API",
    description="API for 3d filaments purpose. Analysis for minor cost",
    version="1.0.0"1
)

app.include_router(filaments.router, prefix="/filaments")

@app.get("/")
async def root():
    return {"message": "You're online ! "}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
