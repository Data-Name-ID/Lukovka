from core.models.jwt import AccessToken, RefreshToken, TokenCollection
from core.models.user import UserCreate, UserLogin, UserPublic
from core.schemas import DetailScheme
from core.store import store
from fastapi import APIRouter, BackgroundTasks, HTTPException, Request
from fastapi.responses import RedirectResponse
from starlette import status

from api.auth import errors
from api.auth.depends import SessionDep, UserDep

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    "/signup",
    summary="Регистрация",
    response_description="Зарегистрированный пользователь",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Пользователь уже зарегистрирован",
            "model": DetailScheme,
        },
    },
)
async def sign_up(
    user_in: UserCreate,
    request: Request,
    background_tasks: BackgroundTasks,
    session: SessionDep,
) -> TokenCollection:
    if await store.user_accessor.user_exists_by_email(
        session=session,
        email=user_in.email,
    ):
        raise errors.USER_ALREADY_EXISTS_ERROR

    user_id = await store.user_accessor.create_user(session=session, user_in=user_in)
    await session.commit()

    background_tasks.add_task(
        store.user_manager.send_confirm_email,
        user_id=user_id,
        user=user_in,
        base_url=request.base_url,
    )
    return store.jwt.create_token_collection(user_id)


@router.post(
    "/signin",
    summary="Вход в систему",
    response_description="Токены доступа",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Неверный email или пароль",
            "model": DetailScheme,
        },
    },
)
async def sign_in(user_in: UserLogin, session: SessionDep) -> TokenCollection:
    user = await store.user_accessor.fetch_user_by_email(
        session=session,
        email=user_in.email,
    )

    if not (user and user.validate_password(user_in.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    return store.jwt.create_token_collection(user.id)


@router.get(
    "/current",
    summary="Текущий пользователь",
    response_description="Текущий пользователь",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Недействительный токен или пользователь не активирован",
            "model": DetailScheme,
        },
    },
)
async def current_user(user: UserDep) -> UserPublic:
    return user


@router.post(
    "/refresh",
    summary="Обновление токена",
    response_description="Новые токены доступа",
    response_model_exclude_defaults=True,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Недействительный токен",
            "model": DetailScheme,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Пользователь не существует",
            "model": DetailScheme,
        },
    },
)
async def refresh(token: RefreshToken, session: SessionDep) -> AccessToken:
    return await store.user_manager.refresh_access_token(
        token=token.refresh_token,
        session=session,
    )


@router.get(
    "/confirm-email",
    summary="Подтверждение email",
    response_description="Перенаправление на главную страницу",
)
async def confirm_email(token: str, session: SessionDep) -> RedirectResponse:
    await store.user_manager.activate_user_by_token(token=token, session=session)
    return RedirectResponse(url="/")
