from fastapi import APIRouter, HTTPException
from app.core.schemas.user import UserCreate, UserInDB
from app.core.services.user_service import get_all_users, get_user, create_user
from typing import List

router = APIRouter()


@router.get("/users/", response_model=List[UserInDB])
async def get_users():
    try:
        response = await get_all_users()
        if response.data:
            return [UserInDB(**user) for user in response.data]
        return []
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/users/{user_id}", response_model=UserInDB)
async def get_user_by_id(user_id: int):
    try:
        response = await get_user(user_id)
        if response.data:
            return UserInDB(**response.data)
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/users/", response_model=UserInDB)
async def create_new_user(user: UserCreate):
    try:
        response = await create_user(user)
        if response.data:
            return UserInDB(**response.data[0])
        raise HTTPException(status_code=400, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
