from fastapi import APIRouter
from services.scraper import get_mercadolivre_filaments
from schemas.filament_price import FilamentPriceSchema

router = APIRouter(tags=["Filament Price"])


@router.get("/mercadolivre", response_model=list[FilamentPriceSchema])
async def get_filaments_mercadolivre():
    return get_mercadolivre_filaments()
