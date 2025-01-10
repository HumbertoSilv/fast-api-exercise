from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_api_exercise.database import get_session
from fast_api_exercise.models.user import User
from fast_api_exercise.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fast_api_exercise.security import (
    get_current_user,
    get_password_hash,
)
from fast_api_exercise.settings import logger

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session):
    logger.debug(f'Starting user creation - {user.email} - {user.username}')

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            logger.error(f'Username already exists - {user.username}')

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            logger.error(f'Email already exists - {user.email}')

            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    # db_user = User(**user.model_dump())
    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    logger.info(f'User created - {db_user.id}')

    return db_user


@router.get('/', response_model=UserList)
def read_users(
    session: T_Session, filter_users: Annotated[FilterPage, Query()]
):
    logger.debug('Starting listing of users')
    users = session.scalars(
        select(User).offset(filter_users.offset).limit(filter_users.limit)
    ).all()

    return {'users': users}


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: T_Session):
    logger.debug(f'Starting user search - {user_id}')

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        logger.error(f'User not found - {user_id}')

        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    logger.debug(f'Starting user update - {user_id} - {user}')

    if current_user.id != user_id:
        logger.error(f'Not enough permissions - {user_id}')

        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        logger.error(f'Username or Email already exists - {user}')

        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    logger.debug(f'Starting user deletion - {user_id}')

    if current_user.id != user_id:
        logger.error(f'Not enough permissions - {user_id}')

        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
