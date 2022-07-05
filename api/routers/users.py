from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datatypes.datatypes import User, UserUpdate
from core.core_functions import (
    is_authentication_successful,
    registering_user,
    get_all_users,
    update_user,
    delete_user,
    is_authentication_successful,
    get_my_user_info,
)

router = APIRouter()
security = HTTPBasic()


@router.post("/users")
def register_user(user: User):
    return registering_user(user)


@router.get("/users")
def get_all_users_(credentials: HTTPBasicCredentials = Depends(security)):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return get_all_users()
    return {"message": "Authentication failure"}


@router.get("/users/me")
def get_my_user_info_(credentials: HTTPBasicCredentials = Depends(security)):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return get_my_user_info(username=credentials.username)
    return {"message": "Authentication failure"}


@router.put("/users/update/{username}")
def update_user_(
    username: str,
    user: UserUpdate,
    credentials: HTTPBasicCredentials = Depends(security),
):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return update_user(username=username, user=user)
    return {"message": "Authentication failure"}


@router.delete("/users/delete/{username}")
def delete_user_(username: str, credentials: HTTPBasicCredentials = Depends(security)):
    if is_authentication_successful(
        username=credentials.username, password=credentials.password
    ):
        return delete_user(username)
    return {"message": "Authentication failure"}
