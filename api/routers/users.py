from fastapi import APIRouter
from datatypes.datatypes import User
from core.core_functions import registering_user, get_all_users

router = APIRouter()


@router.get("/users")
def get_all_users_():
    return get_all_users()


@router.post("/users")
def register_user(user: User):
    return registering_user(user)
