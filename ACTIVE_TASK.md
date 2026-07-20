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

### 📢 Estado Geral: `EM ANDAMENTO`

> [!IMPORTANT]
> Uma varredura inicial revelou que a suíte de testes de integração está passando, porém existem pendências críticas de formatação (Ruff) e tipagem (MyPy) a serem resolvidas.

---

### 1. Tarefa Atual / Contexto
*   **Solicitado por:** Preparação do Repositório (Discovery)
*   **Descrição:** Correção de conformidade com Ruff (94 erros) e MyPy (68 erros de tipagem estática), mantendo todos os 8 testes existentes em execução com sucesso.

### 2. Objetivo Geral
*   [ ] Obter conformidade de 100% no Ruff (`ruff check` e `ruff format` limpos).
*   [ ] Obter conformidade de 100% no MyPy (`mypy app/` sem erros de tipo).
*   [ ] Garantir que 100% dos testes continuem passando (`pytest` 8/8 OK).

### 3. Status de Progresso
*   [x] Mapear estado atual da base de código (Testes passando, linter e types falhando).
*   [ ] Aplicar correções automáticas de importação e estilo com Ruff (`uv run ruff check --fix .` e `uv run ruff format .`).
*   [ ] Corrigir erros de assinatura Pydantic manual (como uso incorreto de `cls` em validators do `app/modules/transactions/schemas.py`).
*   [ ] Resolver as redefinições de nomes de rotas (como `monthly_flow` em `app/modules/cash_flow/router.py`).
*   [ ] Corrigir tipos de anotação de funções inválidas no MyPy (como em `app/modules/categories/schemas.py`).

### 4. Arquivos Modificados / Criados
*Nenhum arquivo modificado ainda nesta tarefa.*

### 5. Próximos Passos Imediatos
1.  Rodar `uv run ruff check --fix .` para sanar a maior parte das quebras de ordenação de imports e formatação.
2.  Rodar `uv run ruff format .` para formatar os arquivos.
3.  Investigar os erros manuais apontados pelo MyPy nas schemas (especialmente os tipos inválidos e a anotação `Money` / `PositiveMoney`).
4.  Resolver a redefinição de `monthly_flow` no roteador do fluxo de caixa.

### 6. Bloqueios e Problemas Conhecidos
*   Não há bloqueios externos, todos os erros são locais e relacionados à estaticidade de código e formatação.

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
