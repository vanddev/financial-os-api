---
name: project-conventions
description: Guidelines and best practices for developing domain modules, handling database sessions, generating migrations, writing tests, and maintaining code quality in the Financial OS API repository.
---

# Padrões e Convenções de Desenvolvimento do Projeto (`project-conventions`)

Esta skill orienta o desenvolvimento e manutenção do repositório **Financial OS API**. Siga estas instruções estritamente para manter a conformidade com a arquitetura e estilo do projeto.

---

## 📂 Arquitetura de Módulos (Domain-Driven)

Todo novo domínio de negócio deve residir em um subdiretório de `app/modules/` contendo:
*   `models.py`: Modelos SQLAlchemy herdando de `app.core.database.Base`.
*   `schemas.py`: Modelos Pydantic v2 para validação e serialização.
*   `services.py`: Lógica de negócio e acesso ao banco. Funções devem aceitar um objeto `db: Session` do SQLAlchemy.
*   `router.py`: Roteador do FastAPI (`APIRouter`) definindo os endpoints da API.
*   `__init__.py`: Importa e expõe o roteador do módulo.

### Exemplo de Roteador (`router.py`)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.your_module import schemas, services

router = APIRouter(prefix="/your-module", tags=["Your Module"])

@router.post("/", response_model=schemas.YourResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: schemas.YourCreate, db: Session = Depends(get_db)):
    return services.create_item(db=db, item_data=item.model_dump())
```

---

## 🗄️ Manipulação de Banco de Dados e SQLAlchemy

1.  **Transações e Sessões:**
    *   Este projeto utiliza sessões **síncronas** (`Session` de `sqlalchemy.orm`).
    *   Utilize a dependência `get_db` em rotas FastAPI para injeção de dependência.
    *   Sempre utilize `db.commit()` e `db.refresh()` dentro dos services ao persistir novos registros.
    *   Certifique-se de liberar os recursos usando blocos `try/finally` caso instancie sessões manualmente (como em scripts utilitários).
2.  **Relacionamentos e Desempenho:**
    *   Utilize SQLAlchemy 2.0 style query queries (ex: `db.scalars(select(Model).where(...)).all()`).
    *   Seja explícito quanto ao carregamento de relacionamentos para evitar consultas N+1 (ex: use `selectinload` ou `joinedload` quando apropriado).

---

## 🚀 Migrações de Banco de Dados (Alembic)

1.  **Geração:**
    *   Toda alteração em `models.py` requer uma nova migração.
    *   Gere a migração com: `uv run alembic revision --autogenerate -m "descrição"`
2.  **Revisão Manual:**
    *   **Nunca** aplique uma migração gerada automaticamente sem antes ler o arquivo gerado em `alembic/versions/`.
    *   Verifique se o Alembic detectou corretamente novos campos, chaves primárias/estrangeiras e índices.
3.  **Execução:**
    *   Aplique as migrações localmente com `uv run alembic upgrade head` antes de subir o servidor ou rodar testes de integração.

---

## 🧪 Qualidade de Código e Testes

1.  **Validação de Sintaxe e Estilo:**
    *   Execute `uv run ruff check .` para verificar erros. Use `--fix` para correções seguras e automáticas.
    *   Execute `uv run ruff format .` para alinhar a formatação do código.
2.  **Tipagem Estática:**
    *   Este projeto exige tipagem estrita com MyPy.
    *   Execute `uv run mypy app/` e garanta que não haja erros de tipagem em qualquer código adicionado.
3.  **Escrevendo Testes:**
    *   Todos os testes devem ser colocados em `app/tests/` com o prefixo `test_`.
    *   Use o cliente de teste assíncrono `AsyncClient` de `httpx` para chamadas HTTP nas rotas da API.
