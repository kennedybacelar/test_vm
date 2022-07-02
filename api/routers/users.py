from fastapi import APIRouter
from datatypes.datatypes import User

router = APIRouter()


@router.post("/users")
def register_user(user: User):
    return "registering user"
