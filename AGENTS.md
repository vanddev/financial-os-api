# Guia de Contexto para Agentes de IA (`AGENTS.md`)

Este arquivo serve como ponto de partida rápido (discovery) para agentes de IA que forem trabalhar neste repositório. Ele resume a arquitetura, as principais tecnologias, padrões de código, comandos úteis e como interagir de forma produtiva com outros agentes e ferramentas.

---

## 🚀 Visão Geral do Projeto

O **Financial OS API** é uma plataforma de finanças pessoais e gerenciamento familiar. Ele expõe uma API RESTful para controle de contas, transações, cartões de crédito, orçamentos, metas, investimentos, assinaturas, fluxo de caixa e patrimônio líquido.

### Stack Tecnológica
*   **Linguagem:** Python 3.13+
*   **Framework Web:** FastAPI (com uvicorn)
*   **Banco de Dados:** PostgreSQL (ORM: SQLAlchemy 2.0)
*   **Gerenciador de Dependências:** `uv` (rápido e moderno)
*   **Migrações:** Alembic
*   **Qualidade e Linter:** Ruff & MyPy
*   **Testes:** Pytest (com httpx para clientes assíncronos)
*   **Orquestração:** Docker & Docker Compose

---

## 📂 Estrutura do Código e Convenções

O projeto segue um padrão **Domain-Driven modular**, onde cada funcionalidade ou domínio de negócio possui seu próprio subdiretório em `app/modules/`.

```
app/
├── core/              # Componentes de infraestrutura base (db, config, exceptions, lifespan)
├── modules/           # Módulos de domínio de negócio (ex: accounts, transactions, goals)
│   └── <modulo>/
│       ├── __init__.py# Exporta o roteador do módulo
│       ├── models.py  # Modelos SQLAlchemy
│       ├── schemas.py # Schemas Pydantic (validação)
│       ├── services.py# Lógica de negócio / consultas ao DB
│       └── router.py  # Endpoints da API (FastAPI)
├── shared/            # Utilitários compartilhados (middlewares, paginação, respostas padrão)
├── tests/             # Testes integrados e unitários
└── main.py            # Inicialização e registro de roteadores
```

### Regras para Criação de Novos Módulos
Ao criar um novo domínio (ex: `insurance` ou `reports`), siga este passo a passo:
1.  Crie a pasta sob `app/modules/your_module`.
2.  Crie os arquivos `models.py`, `schemas.py`, `services.py`, `router.py` e `__init__.py`.
3.  Defina o roteador em `router.py` com o prefixo correto. Ex: `router = APIRouter(prefix="/your-module", tags=["your-module"])`.
4.  Exporte o roteador em `__init__.py` utilizando `__all__ = ["router"]`.
5.  Registre o roteador em `app/main.py` usando `app.include_router(your_module_router)`.
6.  Crie os testes integrados em `app/tests/test_your_module.py`.

---

## 🛠️ Comandos de Desenvolvimento Úteis

Sempre utilize `uv run` para executar comandos dentro do ambiente virtual configurado.

| Ação | Comando |
| :--- | :--- |
| **Subir DB e PgAdmin (Docker)** | `docker compose up postgres pgadmin` |
| **Rodar Servidor Local (Reload)** | `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` |
| **Gerar Migração Alembic** | `uv run alembic revision --autogenerate -m "descrição"` |
| **Aplicar Migrações** | `uv run alembic upgrade head` |
| **Reverter Última Migração** | `uv run alembic downgrade -1` |
| **Popular Banco com Mock Data** | `python scripts/seed_financial.py` |
| **Rodar Testes** | `uv run pytest` |
| **Rodar Cobertura de Testes** | `uv run pytest --cov=app --cov-report=html` |
| **Verificar Linter (Ruff)** | `uv run ruff check .` |
| **Corrigir Automaticamente (Ruff)** | `uv run ruff check --fix .` |
| **Formatar Código (Ruff)** | `uv run ruff format .` |
| **Verificar Tipagem (MyPy)** | `uv run mypy app/` |

---

## 💡 Skills Recomendadas para o Agente

Para garantir que os agentes de IA operem com as melhores práticas recomendadas pelo setor e com segurança, sugerimos ativar ou instalar skills públicas e seguras em seu diretório global (`~/.gemini/config/skills/`) ou usá-las como referência:

1.  **FastAPI & Pydantic v2 Best Practices Skill:**
    *   *Objetivo:* Guia de injeção de dependências no FastAPI (ex: uso correto de `Depends(get_db)`), uso de payloads validados com Pydantic v2 e estruturação de respostas padronizadas.
    *   *Diretório sugerido:* `fastapi-pydantic-v2`
2.  **SQLAlchemy 2.0 Declarative & Session Management Skill:**
    *   *Objetivo:* Instruir o agente a utilizar a nova API do SQLAlchemy 2.0 (como o uso de `select()`, paginação integrada, carregamento de relacionamentos via `joinedload` ou `selectinload` para evitar N+1 query issues).
    *   *Diretório sugerido:* `sqlalchemy-2-conventions`
3.  **Alembic Migration Safety Skill:**
    *   *Objetivo:* Impedir modificações destrutivas na base de dados (como remoção de tabelas ou colunas sem rollback correspondente ou migrações de dados complexas misturadas com DDL).
    *   *Diretório sugerido:* `alembic-migration-safety`
4.  **Pytest Async & DB Mocking Skill:**
    *   *Objetivo:* Instruções para a criação de fixtures limpas para testes de integração, recriação de tabelas temporárias (ou uso de `sqlite` em memória ou PostgreSQL de testes) e mocking de dependências de API.
    *   *Diretório sugerido:* `pytest-clean-testing`

> [!NOTE]
> Você pode configurar essas skills no repositório criando a pasta `.agents/skills/<nome-da-skill>/SKILL.md` para que qualquer agente que abra este repositório herde as instruções automaticamente.

---

## 👥 Fluxo Multiagentes e Acompanhamento de Tarefas

Se você precisar trabalhar em paralelo com outros agentes ou se sua janela de contexto estiver próxima do limite, utilize as diretrizes e arquivos abaixo para coordenar o trabalho de forma fluida:

1.  **Instruções de Coordenação Multiagente:** Consulte o arquivo [MULTIAGENT.md](file:///var/home/vand/dev/financial-os-api/MULTIAGENT.md) para entender como dividir tarefas entre subagentes especialistas e evitar conflitos de código.
2.  **Acompanhamento de Estado e Progresso:** Consulte e mantenha atualizado o arquivo [ACTIVE_TASK.md](file:///var/home/vand/dev/financial-os-api/ACTIVE_TASK.md). Este arquivo mantém o progresso atual, pendências, arquivos alterados e passos imediatos para que o próximo agente possa retomar o trabalho de forma instantânea sem perda de contexto.


## Aprovação obrigatória

  - Não modifique arquivos sem apresentar previamente o plano ou diff proposto.
  - Aguarde aprovação explícita antes de aplicar qualquer alteração.
  - Comandos somente leitura podem ser executados sem aprovação.
  - Não execute migrations nem altere bancos sem aprovação explícita.

<!-- ## Agent Delivery Workflow

Demandas de implementação coordenadas por múltiplos agentes devem seguir
`.agents/README.md`. O fluxo obrigatório separa planejamento e execução:

1. o Orquestrador encaminha a demanda, sem reinterpretá-la, ao Product Manager;
2. o Product Manager inspeciona o repositório e produz ou atualiza
   `handoff.md`, mas não implementa a feature;
3. o Orquestrador só libera tarefas cujo contrato de execução esteja completo;
4. o Developer implementa código e testes dentro da responsabilidade de
   arquivos definida e registra evidências e decisões;
5. o Orquestrador encerra a demanda somente quando aceite, testes e evidências
   forem rastreáveis.

Os perfis ficam em `.agents/profiles/`. O contrato mínimo de uma tarefa inclui
objetivo, escopo e fora de escopo, dependências, responsabilidade exclusiva ou
compartilhada de arquivos, critérios de aceite, cenários de teste, paralelismo,
comandos de verificação e local das evidências. Use
`.agents/templates/handoff.template.md` para novos planejamentos e
`.agents/templates/task-evidence.template.md` para cada entrega. -->