# Acompanhamento de Tarefa Ativa (`ACTIVE_TASK.md`)

Este arquivo é o quadro de estado ativo do repositório. Ele serve para registrar o progresso de tarefas longas, facilitando a troca de turnos entre agentes de IA ou retomada após estouro da janela de contexto.

---

## 📖 Como Usar Este Arquivo (Instruções para o Agente)

1.  **Ao Iniciar uma Tarefa:**
    *   Leia este arquivo para verificar se há alguma tarefa em andamento não finalizada.
    *   Se estiver iniciando uma nova tarefa solicitada pelo usuário, atualize este arquivo com as informações do formulário abaixo.
2.  **Durante a Execução:**
    *   Mantenha a lista de tarefas pendentes e concluídas atualizada conforme o progresso.
3.  **Ao Finalizar um Turno ou Handover (Próximo de Limites de Contexto/Token):**
    *   Atualize a seção **Status de Progresso**, **Arquivos Modificados** e descreva em detalhes os **Próximos Passos** e **Bloqueios**.
    *   Salve o arquivo antes de encerrar o seu turno ou antes do esgotamento da sessão.

---

# 📝 Quadro de Estado Atual

<!-- INÍCIO DO QUADRO DE ESTADO -->

### 📢 Estado Geral: `CONCLUÍDO`

> [!IMPORTANT]
> Uma varredura inicial revelou que a suíte de testes de integração está passando, porém existem pendências críticas de formatação (Ruff) e tipagem (MyPy) a serem resolvidas.

### Incidente concluído: serialização de transações
*   **Problema:** `POST /transactions/` e `PUT /transactions/{tx_id}` retornavam erro 500 ao serializar uma instância ORM de `Transaction`.
*   **Causa:** as rotas usavam `SuccessResponse` sem o tipo genérico de `data`.
*   **Correção:** respostas parametrizadas como `SuccessResponse[TransactionDTO]` e teste HTTP de regressão com o payload reportado.
*   **Validação:** `uv run pytest -q` com 22 testes aprovados; Ruff aprovado nos arquivos alterados.
*   **Arquivos:** `app/modules/transactions/router.py`, `app/tests/test_transactions.py` e `app/tests/conftest.py`.

### Alteração concluída: remoção de `credit_cards.color`
*   **Correção:** campo removido do modelo SQLAlchemy, dos schemas de entrada, do DTO de resposta e dos dados de seed.
*   **Banco:** migração `remove_credit_card_color` remove a coluna no upgrade e a restaura no downgrade.
*   **Validação:** suíte de testes aprovada, regressão de contrato adicionada em `app/tests/test_credit_cards.py` e Ruff limpo em `app/modules/credit_cards`.

---

### 1. Tarefa Atual / Contexto
*   **Solicitado por:** Proteção contra registros financeiros duplicados
*   **Descrição:** Implementar `Idempotency-Key` no `POST /transactions/`.

### 2. Objetivo Geral
*   [x] Exigir a chave no endpoint de criação.
*   [x] Persistir chave e hash do payload com unicidade no banco.
*   [x] Reutilizar a resposta da criação em retries equivalentes.
*   [x] Rejeitar com `409` a mesma chave associada a payload diferente.

### 3. Status de Progresso
*   [x] Mapear arquitetura e contratos existentes.
*   [x] Implementar modelo, repository, service e router.
*   [x] Criar e revisar migração Alembic.
*   [x] Adicionar testes de integração HTTP.
*   [x] Validar testes, Ruff e MyPy no escopo alterado.

### 4. Arquivos Modificados / Criados
* `app/modules/transactions/models.py`
* `app/modules/transactions/repository.py`
* `app/modules/transactions/service.py`
* `app/modules/transactions/router.py`
* `app/tests/test_transactions.py`
* `alembic/versions/20260727_0000_add_transaction_idempotency.py`

### 5. Próximos Passos Imediatos
1. Aplicar `uv run alembic upgrade head` no banco do ambiente.
2. Atualizar frontend e bot para enviar uma chave estável por operação.

### 6. Bloqueios e Problemas Conhecidos
* O worktree contém alterações anteriores da API analítica/MCP que devem ser preservadas.
* Permanecem os débitos globais preexistentes: 111 erros Ruff e 73 erros MyPy.
* Validação desta tarefa: 44 testes aprovados; Ruff e MyPy aprovados no escopo alterado.

### 7. Comandos para Retomada / Verificação
```bash
# Executar testes unitários
uv run pytest

# Executar linter Ruff
uv run ruff check .

# Executar MyPy typecheck
uv run mypy app/
```

<!-- FIM DO QUADRO DE ESTADO -->
