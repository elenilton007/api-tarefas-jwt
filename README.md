# 🔐 API REST de Gerenciamento de Tarefas (com Autenticação JWT)

API RESTful em Python (Flask) para gerenciamento de tarefas, com autenticação segura via **JSON Web Token (JWT)** e isolamento de dados por usuário.

## 📋 Sobre o projeto

Este projeto demonstra a construção de uma API profissional do zero, cobrindo os pilares que toda vaga de backend/desenvolvimento pede:

- Autenticação e autorização (JWT)
- Senhas armazenadas com hash seguro (nunca em texto puro)
- Isolamento de dados entre usuários (um usuário nunca acessa dados de outro)
- Operações CRUD completas
- Testes automatizados cobrindo os cenários críticos de segurança

## 🧠 Arquitetura

| Arquivo | Responsabilidade |
|---|---|
| `schema.sql` | Estrutura do banco (usuários e tarefas) |
| `database.py` | Conexão com o banco de dados (SQLite) |
| `auth.py` | Cadastro e autenticação de usuários (hash de senha) |
| `models.py` | CRUD de tarefas, com filtro obrigatório por usuário |
| `app.py` | Rotas da API e configuração do JWT |
| `tests/test_api.py` | Testes automatizados (incluindo testes de segurança) |

## 🔑 Endpoints

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| POST | `/auth/registrar` | Não | Cadastra novo usuário |
| POST | `/auth/login` | Não | Autentica e retorna token JWT |
| GET | `/tarefas` | Sim | Lista tarefas do usuário logado |
| POST | `/tarefas` | Sim | Cria nova tarefa |
| GET | `/tarefas/<id>` | Sim | Busca uma tarefa específica |
| PUT | `/tarefas/<id>` | Sim | Atualiza uma tarefa |
| DELETE | `/tarefas/<id>` | Sim | Exclui uma tarefa |

## ▶️ Como executar

Instalar dependências: `pip install -r requirements.txt`

Inicializar banco de dados: `python database.py`

Rodar a API: `python app.py` (fica em `http://127.0.0.1:5001`)

Rodar os testes: `pytest tests/ -v`

## 🔒 Segurança aplicada

- Senhas nunca armazenadas em texto puro (hash com Werkzeug/PBKDF2)
- Tokens JWT com expiração (2 horas)
- Toda rota de tarefas exige token válido (`@jwt_required()`)
- Toda consulta ao banco filtra por `usuario_id`, prevenindo acesso cruzado entre contas

## 🔧 Tecnologias

- Python 3, Flask
- Flask-JWT-Extended (autenticação)
- SQLite
- Pytest

## 🚀 Próximos passos

- Refresh tokens
- Rate limiting
- Documentação interativa (Swagger/OpenAPI)
- Deploy em nuvem

## 👤 Autor

**Elenilton Santos da Silveira**
Técnico em Desenvolvimento de Sistemas | Técnico em Automação Industrial
[LinkedIn](https://www.linkedin.com/in/elenilton-santos-da-silveira-450952285)
