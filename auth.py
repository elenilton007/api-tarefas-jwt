"""
auth.py
Lógica de autenticação: cadastro de usuário com senha criptografada (hash)
e verificação de login. Nunca armazenamos senha em texto puro — seguimos
boas práticas de segurança usando hashing (Werkzeug/PBKDF2).
"""

from werkzeug.security import generate_password_hash, check_password_hash

from database import get_connection


class UsuarioJaExisteError(Exception):
    pass


class CredenciaisInvalidasError(Exception):
    pass


def cadastrar_usuario(nome: str, email: str, senha: str) -> int:
    senha_hash = generate_password_hash(senha)
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
                (nome, email, senha_hash),
            )
            return cursor.lastrowid
    except Exception as exc:
        if "UNIQUE" in str(exc):
            raise UsuarioJaExisteError(f"E-mail '{email}' já cadastrado.")
        raise


def autenticar(email: str, senha: str) -> dict:
    """Verifica e-mail/senha e retorna os dados do usuário se válidos."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()

    if row is None or not check_password_hash(row["senha_hash"], senha):
        raise CredenciaisInvalidasError("E-mail ou senha inválidos.")

    return {"id": row["id"], "nome": row["nome"], "email": row["email"]}
