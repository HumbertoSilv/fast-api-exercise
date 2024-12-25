from jwt import decode

from fast_api_exercise.models.user import User
from fast_api_exercise.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_create_access_token():
    # arrange
    data = {'test': 'test'}

    # act
    token = create_access_token(data)
    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    # assert
    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_get_current_user(session, token):
    # act
    user = get_current_user(session, token)

    # assert
    assert isinstance(user, User)


# def test_get_current_user_without_username(session, token):
#     invalid_token = create_access_token({})
#     # act
#     user = get_current_user(session, invalid_token)
#     print(user)

#     # assert
#     assert isinstance(user, User)
