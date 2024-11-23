from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_exercise.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    # arrange
    client = TestClient(app)

    # act
    response = client.get('/')

    # assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'hello!'}
