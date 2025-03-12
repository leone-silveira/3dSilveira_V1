from fastapi import APIRouter
from services.scraper import get_mercadolivre_filaments, get_amazon_filaments
from schemas.filament import FilamentSchema

router = APIRouter()


@router.get("/mercadolivre", response_model=list[FilamentSchema])
async def get_filaments_mercadolivre():
    return get_mercadolivre_filaments()


@router.get("/amazon", response_model=list[FilamentSchema])
async def get_filaments_amazon():
    return get_amazon_filaments()
