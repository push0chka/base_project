from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.app.api.v1.schemas.users import UserResponse, CreateUserRequest
from src.core.domains.user.service import UserService

router = APIRouter(prefix="/users", tags=["users"], route_class=DishkaRoute)


@router.get("", response_model=list[UserResponse])
async def get_users_handler(
    service: FromDishka[UserService],
) -> list[UserResponse]:
    users = await service.get_all()

    return [UserResponse.model_validate(user.model_dump()) for user in users]


@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user_handler(
    user_id: UUID, service: FromDishka[UserService]
) -> UserResponse:
    user = await service.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserResponse(id=user.id, name=user.name)


@router.post("/user", response_model=UserResponse)
async def create_many_users_handler(
    user: CreateUserRequest, service: FromDishka[UserService]
) -> UserResponse:
    user = await service.create(user.name)
    return UserResponse(id=user.id, name=user.name)
