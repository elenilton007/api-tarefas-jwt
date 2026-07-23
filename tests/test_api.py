"""
test_api.py
Testes automatizados da API — cobrem cadastro, login, autenticação JWT,
isolamento de dados entre usuários e operações de CRUD de tarefas.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from database import init_db
import app as api_module


@pytest.fixture()
def client():
    init_db()
    api_module.app.config["TESTING"] = True
    with api_module.app.test_client() as c:
        yield c


def registrar_e_logar(client, email="user@teste.com", senha="senha123"):
    client.post(
        "/auth/registrar",
        json={"nome": "Usuário Teste", "email": email, "senha": senha},
    )
    resp = client.post("/auth/login", json={"email": email, "senha": senha})
    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_registrar_usuario(client):
    resp = client.post(
        "/auth/registrar",
        json={"nome": "Ana", "email": "ana@teste.com", "senha": "123456"},
    )
    assert resp.status_code == 201
    assert resp.get_json()["email"] == "ana@teste.com"


def test_nao_permite_email_duplicado(client):
    client.post(
        "/auth/registrar",
        json={"nome": "Ana", "email": "ana@teste.com", "senha": "123456"},
    )
    resp = client.post(
        "/auth/registrar",
        json={"nome": "Outra Ana", "email": "ana@teste.com", "senha": "999999"},
    )
    assert resp.status_code == 409


def test_login_com_senha_errada(client):
    client.post(
        "/auth/registrar",
        json={"nome": "Ana", "email": "ana@teste.com", "senha": "123456"},
    )
    resp = client.post(
        "/auth/login", json={"email": "ana@teste.com", "senha": "errada"}
    )
    assert resp.status_code == 401


def test_acesso_sem_token_e_negado(client):
    resp = client.get("/tarefas")
    assert resp.status_code == 401


def test_criar_e_listar_tarefa(client):
    headers = registrar_e_logar(client)

    resp = client.post(
        "/tarefas", json={"titulo": "Estudar SQL"}, headers=headers
    )
    assert resp.status_code == 201

    resp = client.get("/tarefas", headers=headers)
    tarefas = resp.get_json()
    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Estudar SQL"


def test_usuario_nao_acessa_tarefa_de_outro(client):
    headers_a = registrar_e_logar(client, email="a@teste.com")
    headers_b = registrar_e_logar(client, email="b@teste.com")

    resp = client.post("/tarefas", json={"titulo": "Tarefa da Ana"}, headers=headers_a)
    tarefa_id = resp.get_json()["id"]

    # Usuário B tenta acessar tarefa do usuário A
    resp = client.get(f"/tarefas/{tarefa_id}", headers=headers_b)
    assert resp.status_code == 404


def test_atualizar_tarefa_como_concluida(client):
    headers = registrar_e_logar(client)
    resp = client.post("/tarefas", json={"titulo": "Fazer commit"}, headers=headers)
    tarefa_id = resp.get_json()["id"]

    resp = client.put(
        f"/tarefas/{tarefa_id}", json={"concluida": True}, headers=headers
    )
    assert resp.status_code == 200
    assert resp.get_json()["concluida"] == 1


def test_excluir_tarefa(client):
    headers = registrar_e_logar(client)
    resp = client.post("/tarefas", json={"titulo": "Tarefa temporária"}, headers=headers)
    tarefa_id = resp.get_json()["id"]

    resp = client.delete(f"/tarefas/{tarefa_id}", headers=headers)
    assert resp.status_code == 204

    resp = client.get(f"/tarefas/{tarefa_id}", headers=headers)
    assert resp.status_code == 404
