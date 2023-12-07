from uuid import uuid4
from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.src.infra.routers.turma_router import router as turma_router
from api.src.infra.routers.usuario_router import router as user_router
from .mocks import *

client = TestClient(turma_router)
client2 = TestClient(user_router)


def test_post_create_a_turma_sucessful():
    response = client.post("/turmas", json=mock_turma)
    assert response.json()['denominacao'] == 'LOP_Orivaldo'
    assert response.status_code == 201


def test_post_add_alunos_to_turma_sucessful():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']
    response = client.post(f'/turmas/{turma_id}/alunos', json=mock_alunos)
    assert response.status_code == 200
    assert response.json() == {'response': 'Os alunos foram cadastrados com sucesso na turma'}


def test_post_add_alunos_to_turma_fail():
    try:
        client.post(f'/turmas/{str(uuid4())}/alunos', json=mock_alunos)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == 'Turma nao encontrada'


def test_post_set_docente_in_turma_sucessful():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']

    response = client2.post("/user", json=mock_user)
    user_discord_id = response.json()['discord_id']
    client2.put(f'/user/grant/{user_discord_id}/DOCENTE')

    response = client.put(f'/turmas/{turma_id}/docente/{user_discord_id}')
    assert response.status_code == 200
    assert response.json() == {'response': 'O docente foi definido como professor da turma'}


def test_post_add_minitestes_to_turma_sucessful():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']
    response = client.post(f'/turmas/{turma_id}/minitestes', json=mock_testes)
    assert response.status_code == 200
    assert response.json() == {'response': 'Os minitestes foram adicionados com sucesso na turma'}


def test_post_add_minitestes_to_turma_fail():
    try:
        client.post(f'/turmas/{str(uuid4())}/minitestes', json=mock_testes)
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == 'Turma nao encontrada'


def test_post_registrar_presenca():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']

    client2.post(f'/user/register/{turma_id}', json=mock_register)

    response = client.post(f'/turmas/{turma_id}/user/334455/presenca')

    assert response.status_code == 200
    assert response.json() == {'response': 'Presença registrada com sucesso'}

    try:
        client.post(f'/turmas/{turma_id}/user/334455/presenca')
    except HTTPException as e:
        assert e.status_code == 409


def test_post_responder_miniteste_sucessful():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']

    client.post(f'/turmas/{turma_id}/minitestes', json=mock_testes)

    client2.post(f'/user/register/{turma_id}', json=mock_register)

    response = client.post(f'/turmas/{turma_id}/user/334455/miniteste', json=mock_teste_resposta_correta)

    assert response.status_code == 200
    assert response.json() == {'response': True}


def test_post_responder_miniteste_fail():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']

    client.post(f'/turmas/{turma_id}/minitestes', json=mock_testes)

    client2.post(f'/user/register/{turma_id}', json=mock_register)

    response = client.post(f'/turmas/{turma_id}/user/334455/miniteste', json=mock_teste_resposta_errada)

    assert response.status_code == 200
    assert response.json() == {'response': False}


def test_get_presenca_turma():
    response = client.post("/turmas", json=mock_turma)
    res_body = response.json()
    turma_id = res_body['turma_id']

    client2.post(f'/user/register/{turma_id}', json=mock_register)

    client.post(f'/turmas/{turma_id}/user/334455/presenca')

    response = client.get(f'/turmas/{turma_id}/presenca')

    assert len(response.json()[0]['frequencia']) == 1
    assert response.status_code == 200

    client.get(f'/turmas/{turma_id}/presenca')
    assert len(response.json()[0]['frequencia']) == 1
