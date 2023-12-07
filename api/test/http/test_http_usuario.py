from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.src.infra.routers.turma_router import router as turma_router
from api.src.infra.routers.usuario_router import router as user_router
from .mocks import *

client = TestClient(user_router)
client2 = TestClient(turma_router)


def test_post_create_an_user_sucessful():
    response = client.post("/user", json=mock_user)
    assert response.status_code == 201
    assert response.json()['id'] is not None
    assert response.json()['discord_id'] == '112233'


def test_post_subscriber_an_user_sucessful():
    response = client2.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']
    response = client.post(f'/user/register/{turma_id}', json=mock_register)
    assert response.status_code == 201
    assert response.json() == {'response': 'Usuario 334455 foi registrado'}


def test_post_grant_role_to_user_sucessful():
    response = client.post("/user", json=mock_user)
    discord_id = response.json()['discord_id']
    role = 'DOCENTE'
    response = client.put(f'/user/grant/{discord_id}/{role}')
    assert response.status_code == 200
    assert response.json() == {'response': f'User {discord_id} role updated'}


def test_post_grant_role_to_user_fail_when_user_not_found():
    role = 'DOCENTE'
    try:
        client.put(f'/user/grant/abc/{role}')
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == 'Usuario nao encontrado'


def test_post_grant_role_to_user_fail_when_role_dont_exist():
    response = client.post("/user", json=mock_user)
    discord_id = response.json()['discord_id']
    role = 'whatever'
    try:
        client.put(f'/user/grant/{discord_id}/{role}')
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == 'Role nao encontrada'


def test_post_revoke_role_to_user_sucessful():
    response = client.post("/user", json=mock_user)
    discord_id = response.json()['discord_id']
    role = 'DOCENTE'
    client.put(f'/user/grant/{discord_id}/{role}')
    response = client.put(f'/user/revoke/{discord_id}/{role}')
    assert response.status_code == 200
    assert response.json() == {'response': f'User {discord_id} role updated'}


def test_post_revoke_role_to_user_fail_when_user_not_found():
    role = 'DOCENTE'
    try:
        client.put(f'/user/revoke/abc/{role}')
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == 'Usuario nao encontrado'
