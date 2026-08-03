# Handoff — <nome da demanda>

> **ID:** `<delivery-id>`
> **Estado:** `draft | ready | in_progress | acceptance | done | blocked`
> **Criado/atualizado:** `<AAAA-MM-DD>`
> **Planejado por:** Product Manager
> **Fonte da demanda:** `<link, issue ou texto abaixo>`

## 1. Demanda original

> <Preservar o texto do solicitante sem reinterpretá-lo.>

## 2. Objetivo e resultado observável

<Descrever o estado final percebido pelo usuário ou sistema.>

### Dentro do escopo

- <item>

### Fora do escopo

- <item>

### Definition of Done da demanda

- [ ] <resultado final comprovável>

## 3. Diagnóstico do repositório

### Baseline observado

- <fluxo, arquivos, comportamento e testes atuais>

### Fontes de verdade e contratos

| Assunto | Fonte | Versão/data | Impacto |
| --- | --- | --- | --- |
| <assunto> | `<arquivo/URL>` | <versão> | <impacto> |

### Comandos de baseline

| Comando | Resultado esperado/observado |
| --- | --- |
| `<comando>` | <resultado> |

### Restrições e riscos conhecidos

- <restrição ou risco>

## 4. Decisões e bloqueios

### Decisões confirmadas

| ID | Decisão | Fonte/responsável | Consequência |
| --- | --- | --- | --- |
| D-01 | <decisão> | <fonte> | <consequência> |

### Perguntas bloqueantes

| ID | Pergunta | Responsável | Tarefas bloqueadas | Mitigação |
| --- | --- | --- | --- | --- |
| B-01 | <pergunta> | <pessoa/sistema> | T-<n> | <se houver> |

## 5. Arquitetura da entrega

<Resumo das fronteiras e do fluxo proposto. Use diagrama apenas se ajudar.>

```text
<componente A> -> <componente B> -> <componente C>
```

## 6. Dependências, ondas e paralelismo

```text
T-01
  ├─ T-02
  └─ T-03
       └─ T-04
```

| Onda | Tarefas | Pode executar em paralelo? | Gate para iniciar | Ordem de integração |
| --- | --- | --- | --- | --- |
| 1 | T-01 | não | <gate> | T-01 |
| 2 | T-02, T-03 | sim, sem sobreposição | T-01 aceita | T-02 → T-03 |

### Matriz global de responsabilidade de arquivos

| Caminho/padrão | Tarefa dona | Exclusivo na onda? | Regra |
| --- | --- | --- | --- |
| `<path>` | T-01 | sim | <regra> |

## 7. Tarefas

### T-01 — <título orientado a resultado>

**Estado:** `draft`
**Onda:** 1
**Objetivo:** <comportamento observável entregue por esta tarefa>

**Dependências e pré-condições:**

- <dependência aceita ou condição verificável>

**Escopo:**

- <item incluído>

**Fora de escopo:**

- <item explicitamente excluído>

**Responsabilidade de arquivos:**

- Exclusivos: `<path>`
- Compartilhados: `<path>` — <regra de coordenação>
- Proibidos: `<path>`

**Passos de implementação:**

1. <passo concreto>
2. <passo concreto>

**Critérios de aceite:**

- AC-01: Dado <estado>, quando <ação>, então <resultado mensurável>.
- AC-02: <critério binário e observável>.

**Cenários de teste:**

| ID | Nível | Cenário | Preparação | Ação | Resultado esperado | Prova de AC |
| --- | --- | --- | --- | --- | --- | --- |
| TS-01 | unitário | caminho feliz | <given> | <when> | <then> | AC-01 |
| TS-02 | unitário | entrada inválida | <given> | <when> | <then> | AC-02 |
| TS-03 | integração | integração da onda | <given> | <when> | <then> | AC-01 |

**Comandos de verificação:**

```bash
<comando focado>
<comando de regressão>
```

**Evidências esperadas:**

- relatório: `evidence/T-01.md`;
- testes: `<arquivo ou comportamento>`;
- inspeções adicionais: `<busca, schema, exemplo sanitizado>`.

**Paralelismo e integração:**

- Pode executar com: <tarefas ou "nenhuma">.
- Não pode executar com: <tarefas e motivo>.
- Gate pós-integração: <teste/comando>.

**Riscos e rollback/mitigação:**

- <risco> → <mitigação ou forma de reversão>.

---

<!-- Repetir a seção para T-02, T-03 etc. -->

## 8. Estratégia de integração

1. <ordem de merge/aplicação>
2. <verificação depois de cada onda>
3. <verificação final>

## 9. Matriz final de rastreabilidade

| Requisito da demanda | Tarefa | Critério de aceite | Cenário/prova |
| --- | --- | --- | --- |
| <requisito> | T-01 | AC-01 | TS-01 |

## 10. Checklist final do Orquestrador

- [ ] Todas as tarefas necessárias estão `accepted`.
- [ ] Todos os critérios possuem evidência reproduzível.
- [ ] Testes focados, integração e regressão foram executados.
- [ ] Decisões arquiteturais estão registradas.
- [ ] Falhas e pendências externas estão explícitas.
- [ ] Nenhuma tarefa paralela deixou conflito ou contrato divergente.
- [ ] O resultado observável da demanda foi verificado.
