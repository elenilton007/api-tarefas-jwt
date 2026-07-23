"""
models.py
Operações de CRUD das tarefas. Toda consulta é filtrada por usuario_id,
garantindo que um usuário nunca acesse tarefas de outro (isolamento de dados
por usuário — princípio básico de segurança em APIs multiusuário).
"""

from database import get_connection


def criar_tarefa(usuario_id: int, titulo: str, descricao: str = "") -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tarefas (usuario_id, titulo, descricao) VALUES (?, ?, ?)",
            (usuario_id, titulo, descricao),
        )
        return cursor.lastrowid


def listar_tarefas(usuario_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY criado_em DESC",
            (usuario_id,),
        ).fetchall()
        return [dict(row) for row in rows]


def buscar_tarefa(usuario_id: int, tarefa_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?",
            (tarefa_id, usuario_id),
        ).fetchone()
        return dict(row) if row else None


def atualizar_tarefa(
    usuario_id: int,
    tarefa_id: int,
    titulo: str | None = None,
    descricao: str | None = None,
    concluida: bool | None = None,
) -> bool:
    tarefa = buscar_tarefa(usuario_id, tarefa_id)
    if tarefa is None:
        return False

    novo_titulo = titulo if titulo is not None else tarefa["titulo"]
    nova_descricao = descricao if descricao is not None else tarefa["descricao"]
    nova_concluida = int(concluida) if concluida is not None else tarefa["concluida"]

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE tarefas
            SET titulo = ?, descricao = ?, concluida = ?
            WHERE id = ? AND usuario_id = ?
            """,
            (novo_titulo, nova_descricao, nova_concluida, tarefa_id, usuario_id),
        )
    return True


def excluir_tarefa(usuario_id: int, tarefa_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
            (tarefa_id, usuario_id),
        )
        return cursor.rowcount > 0
