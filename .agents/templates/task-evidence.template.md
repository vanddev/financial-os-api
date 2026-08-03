# Evidência — <task-id>: <título>

> **Estado:** `implemented | blocked`
> **Developer:** <agente>
> **Início/fim:** <timestamps ou datas>
> **Plano:** `handoff.md#<âncora-da-tarefa>`

## Resultado entregue

<Descrever o comportamento observável implementado, sem repetir apenas passos.>

## Arquivos

| Arquivo | Ação | Motivo |
| --- | --- | --- |
| `<path>` | criado/alterado/removido | <motivo> |

### Conferência de responsabilidade

- [ ] Todos os arquivos estavam atribuídos à tarefa.
- [ ] Alterações preexistentes ou de outros agentes foram preservadas.
- [ ] Qualquer exceção foi autorizada e registrada abaixo.

## Matriz de aceite e evidência

| Critério | Estado | Prova | Resultado |
| --- | --- | --- | --- |
| AC-01 | passou/falhou/bloqueado | `TS-01`, `<comando>` ou inspeção | <resumo objetivo> |

## Testes e verificações

| Comando exato | Código de saída | Resultado resumido |
| --- | --- | --- |
| `<comando>` | 0 | <N testes passaram em Xs> |

### Testes não executados

- <comando/cenário> — <motivo e impacto>, ou "nenhum".

Não colar logs extensos nem conteúdo sensível. Quando uma saída for necessária,
registrar apenas o trecho sanitizado que comprova o resultado.

## Decisões tomadas durante a execução

| ID | Decisão | Alternativas | Motivo | Consequência | ADR |
| --- | --- | --- | --- | --- | --- |
| E-01 | <decisão local> | <alternativas> | <motivo> | <impacto> | `<path ou n/a>` |

## Desvios do plano

- <desvio, autorização e impacto>, ou "nenhum".

## Falhas preexistentes e limitações

- <falha, comando que a demonstra e impacto>, ou "nenhuma".

## Segurança e dados

- [ ] Nenhum serviço real foi chamado, salvo autorização explícita no plano.
- [ ] Nenhum segredo, dado pessoal ou payload de produção foi registrado.
- [ ] Respostas e logs de erro permanecem sanitizados quando aplicável.

## Pendências e handoff

- <pendência, responsável e condição de desbloqueio>, ou "nenhuma".

## Parecer do Developer

`implemented` ou `blocked`: <justificativa curta baseada nas evidências>.

> O estado `accepted` é atribuído exclusivamente pelo Orquestrador após revisar
> este relatório e reproduzir as verificações necessárias.
