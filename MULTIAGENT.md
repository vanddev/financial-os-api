# Diretrizes para Fluxo Multiagentes (`MULTIAGENT.md`)

Este repositório foi estruturado para suportar fluxos de trabalho coordenados por múltiplos agentes de IA de forma eficiente e sem conflitos. Use estas diretrizes para instanciar subagentes especialistas, dividir responsabilidades e consolidar resultados.

---

## 👥 Papéis de Subagentes Especialistas

Quando o agente principal lidar com tarefas complexas, recomenda-se criar subagentes especializados (utilizando a ferramenta `define_subagent` e `invoke_subagent`) para focar em tarefas isoladas:

1.  **DB & Migration Specialist (Especialista em BD):**
    *   *Escopo:* Declaração de modelos SQLAlchemy em `models.py` e geração/revisão de migrações com Alembic.
    *   *Responsabilidade:* Garantir integridade referencial, tipos corretos e migrações que não causem perda de dados.
2.  **API Router & Schema Designer (Desenvolvedor de API):**
    *   *Escopo:* Criação de esquemas Pydantic em `schemas.py` e rotas do FastAPI em `router.py`.
    *   *Responsabilidade:* Validar payloads de entrada e garantir respostas de API padronizadas conforme o resto do app.
3.  **QA & Integration Test Runner (Agente de Testes):**
    *   *Escopo:* Escrita de testes unitários e de integração em `app/tests/`.
    *   *Responsabilidade:* Cobrir caminhos felizes e infelizes (erros), garantindo que os novos endpoints não quebrem endpoints existentes.
4.  **Linter & Type Compliance Inspector (Inspetor de Qualidade):**
    *   *Escopo:* Execução do Ruff e MyPy.
    *   *Responsabilidade:* Garantir que todo código modificado siga as regras de linting (`ruff check .`) e tipagem estrita (`mypy app/`).

---

## ⚙️ Modos de Workspace do Subagente

Ao invocar subagentes com `invoke_subagent`, escolha o modo de workspace apropriado para o caso de uso:

*   **`inherit` (Padrão):** O subagente compartilha o mesmo contexto de diretório e ramificação do agente pai. Use para tarefas pequenas e complementares (ex: pedir para um agente paralelo escrever testes enquanto você finaliza a lógica do service).
*   **`share`:** Cria uma árvore de trabalho separada (similar a um *git worktree*), compartilhando o repositório subjacente. Excelente para trabalhar em módulos de domínio independentes de forma simultânea.
*   **`branch`:** Cria um workspace isolado e clonado. Recomendado para refatorações profundas ou experimentos arriscados que exigem validação antes da fusão.

---

## ⚠️ Prevenção de Conflitos (Crítico)

Trabalhar com múltiplos agentes simultâneos exige cuidado redobrado para evitar sobreposição ou quebra de fluxo:

### 1. Conflitos de Migração no Alembic
*   **Problema:** Dois agentes gerando migrações em paralelo criarão forks na árvore do Alembic (múltiplas revisões apontando para o mesmo `down_revision`).
*   **Regra:** Apenas **um** agente por vez deve rodar `alembic revision --autogenerate`. Se houver migrações geradas simultaneamente em branches separadas, o agente integrador deve fazer o merge das branches e rodar `alembic merge` ou reorganizar as revisões sequencialmente antes do push.

### 2. Escrita Concorrente no Mesmo Arquivo
*   **Regra:** Agentes trabalhando em paralelo não devem editar o mesmo arquivo ao mesmo tempo. Divida as tarefas de forma que cada agente trabalhe em arquivos diferentes (ex: Agente A trabalha em `router.py`, Agente B em `services.py`).
*   **Uso de Ferramentas:** Utilize `multi_replace_file_content` para edições não-contíguas caso edições concorrentes pequenas sejam estritamente necessárias.

### 3. Protocolo de Comunicação e Resoluções
*   Não faça loops ou chamadas recorrentes perguntando o status de um subagente.
*   Use a ferramenta `send_message` para mandar instruções iniciais e aguarde de forma assíncrona. O sistema irá notificar e acordar você assim que o subagente terminar ou reportar progresso.
*   Antes de reportar a conclusão de uma tarefa multiagente ao usuário, o agente principal **deve** rodar a suite de testes inteira (`uv run pytest`) e checar linter/tipagem.
