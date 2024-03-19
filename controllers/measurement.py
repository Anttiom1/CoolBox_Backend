from fastapi import APIRouter

router = APIRouter(
    prefix="/api/test",
    tags="test"
)

@router.get("/testing2")
async def get_testing():
    return {"qwe": "rty"}