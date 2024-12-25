from http import HTTPStatus

from freezegun import freeze_time

from fast_api_exercise.security import create_access_token


def test_get_jwt_token(client, user):
    # act
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    # assert
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_jwt_invalid_token(client):
    # act
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid_token'},
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_without_username_in_token(client):
    # arrange
    data = {'no-email': 'test'}
    invalid_token = create_access_token(data)

    # act
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {invalid_token}'},
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_with_invalid_user_in_token(client):
    # arrange
    data = {'sub': 'invalid_user@example.com'}
    invalid_token = create_access_token(data)

    # act
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {invalid_token}'},
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_jwt_token_with_inexistent_user(client):
    # act
    response = client.post(
        '/auth/token',
        data={'username': 'inexistent_user', 'password': 'test123'},
    )

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_jwt_token_with_invalid_password(client, user):
    # act
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'invalid_password'},
    )

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_expired_after_time(client, user):
    with freeze_time('2023-12-11 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        token = response.json()['access_token']

    with freeze_time('2023-12-11 12:31:00'):
        response = client.delete(
            f'/users/{user.id}/',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Signature has expired'}


def test_refresh_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2024-12-11 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-12-11 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Signature has expired'}
