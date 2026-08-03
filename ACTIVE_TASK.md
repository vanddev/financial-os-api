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

### 📢 Estado Geral: `PLANO PRONTO`

> [!IMPORTANT]
> Demanda ativa `FOS-2026-07-29-DATA-2026`: o refinamento restringiu a entrega
> exclusivamente a `scripts/seed_financial.py`. O banco será reconstruído pelo
> usuário; banco, migrações, fixtures e testes não podem ser alterados.

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
*   **Solicitado por:** usuário
*   **Descrição original:** “atualize todos os dados do banco de dados para
    2026 para evitar problemas nos testes”
*   **Refinamento:** somente `scripts/seed_financial.py`; converter anos 2025 e
    2027 para 2026 preservando mês/dia/horário e demais dados.
*   **Fase:** PLANNING concluído; T-01 está `ready` para PLAN_REVIEW.

### 2. Objetivo Geral
*   [x] Restringir produto exclusivamente ao seed.
*   [x] Confirmar conversão mecânica de 2025/2027 para 2026.
*   [ ] Atualizar apenas chamadas `datetime(...)` do seed.
*   [ ] Validar por AST, compilação, Ruff e revisão do diff.
*   [ ] Registrar evidência; o usuário reconstruirá o banco depois.

### 3. Status de Progresso
*   [x] Ler fluxo multiagente, perfil de Product Manager, templates e skill do projeto.
*   [x] Confirmar ausência de `handoff.md` anterior.
*   [x] Mapear datas no seed, modelos, routers e testes.
*   [x] Coletar baseline de 65 testes com cache `uv` em `/tmp`.
*   [x] Criar contrato completo em `handoff.md`.
*   [x] Incorporar refinamento e resolver bloqueios materiais.
*   [x] Reduzir o plano a uma única tarefa sem sobreposição.
*   [ ] Orquestrador mover T-01 de `ready` para `in_progress`.

### 4. Arquivos Modificados / Criados
* `handoff.md` — criado e refinado, ID `FOS-2026-07-29-DATA-2026`.
* `ACTIVE_TASK.md` — atualizado para o plano pronto.
* Nenhum código, teste, seed, migração ou banco foi alterado nesta fase.

### 5. Próximos Passos Imediatos
1. Orquestrador executar PLAN_REVIEW e atribuir T-01.
2. Developer alterar somente `scripts/seed_financial.py`.
3. Developer registrar `evidence/T-01.md` e validações somente leitura.
4. Orquestrador aceitar; usuário reconstruirá o banco fora da entrega.

### 6. Bloqueios e Problemas Conhecidos
* Nenhum bloqueio de contrato permanece.
* O seed atual apaga várias tabelas; sua execução está fora da entrega.
* Datas 2025/2027 devem mudar apenas no primeiro argumento de `datetime(...)`.
* Ocorrências de ano em nomes/textos e fora do seed não pertencem ao escopo.
* O worktree contém alterações anteriores em `AGENTS.md`, `app/core/config.py`
  e `.agents/`, que devem ser preservadas.

### 7. Comandos para Retomada / Verificação
```bash
rg -n 'datetime\((2025|2027),' scripts/seed_financial.py
UV_CACHE_DIR=/tmp/financial-os-uv-cache uv run python -m py_compile scripts/seed_financial.py
UV_CACHE_DIR=/tmp/financial-os-uv-cache uv run ruff check scripts/seed_financial.py
```

### 8. Histórico relevante preservado
* A demanda anterior de remoção de cores foi registrada como concluída neste
  quadro: campos removidos de accounts/categories/goals/credit_cards, seed e
  testes atualizados, com migrações reversíveis.
* Na entrega anterior foram registrados débitos globais preexistentes de Ruff e
  MyPy e alterações analíticas/MCP no worktree; eles não pertencem à demanda
  temporal atual.

<!-- FIM DO QUADRO DE ESTADO -->
