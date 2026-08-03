## Agent Delivery Workflow

Demandas de implementação coordenadas por agentes seguem
`.agents/README.md`.

O Orquestrador deve encaminhar a demanda ao Product Manager antes de liberar
execução. O Product Manager pode criar ou atualizar o `handoff.md`, mas não
implementa a feature. Developers recebem somente tarefas `ready`, implementam
código e testes dentro da responsabilidade de arquivos definida e registram a
entrega em `evidence/<task-id>.md`. Somente o Orquestrador aceita uma tarefa
depois de confrontar critérios de aceite, testes e evidências.

Todo agente deve ler `AGENTS.md`, `.agents/README.md`, seu perfil em
`.agents/profiles/` e a tarefa completa no `handoff.md` antes de agir.
