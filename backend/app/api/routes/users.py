from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get('/')
def test():
    return {"Users": "API"}
