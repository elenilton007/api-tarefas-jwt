"""
app.py
API REST de Gerenciamento de Tarefas, com autenticação via JWT (JSON Web
Token) — o mesmo padrão usado em APIs profissionais para proteger rotas
sem precisar manter sessão no servidor.

Fluxo de autenticação:
    1. Usuário se cadastra (/auth/registrar)
    2. Usuário faz login (/auth/login) e recebe um token JWT
    3. Usuário envia esse token no header Authorization em toda requisição
       às rotas protegidas (/tarefas/*)
"""

from datetime import timedelta

from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

import auth
import models
from database import init_db

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "chave-secreta-de-demonstracao-trocar-em-producao"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
jwt = JWTManager(app)


# ------------------------------------------------------------------ #
# Autenticação
# ------------------------------------------------------------------ #

@app.route("/auth/registrar", methods=["POST"])
def registrar():
    dados = request.get_json() or {}
    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "nome, email e senha são obrigatórios"}), 400

    try:
        usuario_id = auth.cadastrar_usuario(nome, email, senha)
    except auth.UsuarioJaExisteError as exc:
        return jsonify({"erro": str(exc)}), 409

    return jsonify({"id": usuario_id, "nome": nome, "email": email}), 201


@app.route("/auth/login", methods=["POST"])
def login():
    dados = request.get_json() or {}
    email = dados.get("email")
    senha = dados.get("senha")

    try:
        usuario = auth.autenticar(email, senha)
    except auth.CredenciaisInvalidasError as exc:
        return jsonify({"erro": str(exc)}), 401

    token = create_access_token(identity=str(usuario["id"]))
    return jsonify({"access_token": token, "usuario": usuario}), 200


# ------------------------------------------------------------------ #
# Tarefas (rotas protegidas — exigem token JWT válido)
# ------------------------------------------------------------------ #

@app.route("/tarefas", methods=["GET"])
@jwt_required()
def listar():
    usuario_id = int(get_jwt_identity())
    return jsonify(models.listar_tarefas(usuario_id)), 200


@app.route("/tarefas", methods=["POST"])
@jwt_required()
def criar():
    usuario_id = int(get_jwt_identity())
    dados = request.get_json() or {}
    titulo = dados.get("titulo")

    if not titulo:
        return jsonify({"erro": "titulo é obrigatório"}), 400

    tarefa_id = models.criar_tarefa(
        usuario_id, titulo, dados.get("descricao", "")
    )
    return jsonify({"id": tarefa_id, "titulo": titulo}), 201


@app.route("/tarefas/<int:tarefa_id>", methods=["GET"])
@jwt_required()
def buscar(tarefa_id):
    usuario_id = int(get_jwt_identity())
    tarefa = models.buscar_tarefa(usuario_id, tarefa_id)
    if tarefa is None:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa), 200


@app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
@jwt_required()
def atualizar(tarefa_id):
    usuario_id = int(get_jwt_identity())
    dados = request.get_json() or {}

    sucesso = models.atualizar_tarefa(
        usuario_id,
        tarefa_id,
        titulo=dados.get("titulo"),
        descricao=dados.get("descricao"),
        concluida=dados.get("concluida"),
    )
    if not sucesso:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(models.buscar_tarefa(usuario_id, tarefa_id)), 200


@app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
@jwt_required()
def excluir(tarefa_id):
    usuario_id = int(get_jwt_identity())
    sucesso = models.excluir_tarefa(usuario_id, tarefa_id)
    if not sucesso:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)
