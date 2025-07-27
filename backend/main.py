from fastapi import FastAPI
import uvicorn
from routers import filament_stock, filaments_prices, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Filament API",
    description="API for 3d filaments purpose. Analysis for minor cost",
    version="1.0.0"
)

app.include_router(filaments_prices.router, prefix="/filaments_prices")
app.include_router(filament_stock.router, prefix="/filaments_stock")
app.include_router(user.router, prefix="/users")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5002", "http://localhost:5002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "You're online ! "}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
