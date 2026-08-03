# Handoff — Atualização do seed financeiro para 2026

> **ID:** `FOS-2026-07-29-DATA-2026`
> **Estado:** `ready`
> **Criado/atualizado:** `2026-07-29`
> **Planejado por:** Product Manager
> **Fonte da demanda:** textos do solicitante reproduzidos abaixo

## 1. Demanda original e refinamento

> atualize todos os dados do banco de dados para 2026 para evitar problemas nos testes

> Esses dados persistidos estao nos arquivos de seed, como o banco esta em
> estagio de desenvolvimento atualize apenas o arquivo seed_financial.py que o
> banco sera reconstruido para refletir esses novos dados

## 2. Objetivo e resultado observável

Fazer com que todas as datas de domínio declaradas no seed financeiro pertençam
ao ano de 2026. Datas atualmente em 2025 ou 2027 devem ter somente o ano
substituído por 2026, preservando mês, dia, horário e todos os demais campos. O
usuário reconstruirá o banco posteriormente.

### Dentro do escopo

- Alterar exclusivamente `scripts/seed_financial.py`.
- Converter para 2026 todas as instâncias `datetime(...)` de dados persistidos
  pelo seed que atualmente usam 2025 ou 2027.
- Validar por inspeção e comandos, sem editar testes.
- Registrar evidência documental em `evidence/T-01.md`.

### Fora do escopo

- Executar o seed, reconstruir ou consultar qualquer banco.
- Criar migração ou alterar schema, modelos, routers, configuração ou Docker.
- Alterar fixtures ou testes.
- Alterar mês, dia, horário, valores, textos, status ou relacionamentos.
- Alterar anos que façam parte de nomes/textos, como `Honda Civic 2022` e
  `TESOURO IPCA 2035`.
- Corrigir outras ocorrências de 2025 fora do seed.

### Definition of Done da demanda

- [ ] `scripts/seed_financial.py` não contém `datetime` de dados persistidos com
      ano diferente de 2026.
- [ ] Mês, dia, horário e todos os campos não temporais permanecem inalterados.
- [ ] Nenhum arquivo de produto além do seed foi alterado pela tarefa.
- [ ] Validações de sintaxe, Ruff e inspeção temporal passam.
- [ ] A evidência reproduzível está registrada em `evidence/T-01.md`.

## 3. Diagnóstico do repositório

### Baseline observado

- `scripts/seed_financial.py` é a fonte confirmada pelo solicitante para os
  dados persistidos de desenvolvimento.
- O seed possui datas em 2025 para 7 assinaturas, 2 metas e 17 transações.
- O seed possui datas em 2026 para 2 metas e em 2027 para 1 meta.
- Portanto, 27 valores `datetime(...)` de domínio devem resultar em 2026:
  26 conversões de 2025/2027 e 2 valores já em 2026? A contagem textual inicial
  indica 29 ocorrências no total; o Developer deve usar a inspeção automatizada
  como fonte final e registrar a contagem exata, sem ampliar o escopo.
- O script apaga e recria dados, mas sua execução foi explicitamente atribuída
  ao usuário e não faz parte desta entrega.
- O worktree contém alterações preexistentes fora do seed, que devem ser
  preservadas.

### Fontes de verdade e contratos

| Assunto | Fonte | Versão/data | Impacto |
| --- | --- | --- | --- |
| Escopo exclusivo | Refinamento do solicitante | 2026-07-29 | Somente o seed pode ser alterado |
| Regra de conversão | Demanda original + refinamento | 2026-07-29 | Todo `datetime` persistido fica em 2026, preservando demais componentes |
| Dados de desenvolvimento | `scripts/seed_financial.py` | inspeção 2026-07-29 | Único arquivo de produto da entrega |
| Reconstrução do banco | Refinamento do solicitante | 2026-07-29 | Responsabilidade externa à entrega |

### Comandos de baseline

| Comando | Resultado esperado/observado |
| --- | --- |
| `rg -n 'datetime\\((2025|2027),' scripts/seed_financial.py` | Encontrou datas de assinaturas, metas e transações a converter |
| `rg -n 'datetime\\(2026,' scripts/seed_financial.py` | Encontrou metas já em 2026 |
| `UV_CACHE_DIR=/tmp/financial-os-uv-cache uv run pytest --collect-only -q` | Código 0; 65 testes coletados, sem modificar testes |

### Restrições e riscos conhecidos

- O seed é destrutivo quando executado; a tarefa não deve executá-lo.
- Busca textual ampla também encontra anos legítimos em nomes e valores; o
  aceite considera apenas o primeiro argumento de `datetime(...)`.
- Não se deve editar routers com ocorrências de 2025, pois o refinamento
  restringiu explicitamente o arquivo permitido.

## 4. Decisões e bloqueios

### Decisões confirmadas

| ID | Decisão | Fonte/responsável | Consequência |
| --- | --- | --- | --- |
| D-01 | Alterar somente `scripts/seed_financial.py` | Solicitante, 2026-07-29 | Todos os outros arquivos de produto/teste são proibidos |
| D-02 | Converter 2025 e 2027 para 2026 preservando mês/dia/horário e demais campos | Demanda literal confirmada pelo Orquestrador | Mudança mecânica e verificável |
| D-03 | Não executar nem alterar diretamente o banco | Solicitante, 2026-07-29 | Reconstrução será feita externamente pelo usuário |
| D-04 | Não criar ou editar testes/fixtures | Solicitante, 2026-07-29 | Aceite por inspeção, compilação e Ruff |

### Perguntas bloqueantes

Nenhuma.

## 5. Arquitetura da entrega

```text
scripts/seed_financial.py
  -> conversão mecânica do ano em datetime de domínio
  -> inspeção AST/textual + sintaxe + Ruff
  -> usuário reconstrói o banco (fora desta entrega)
```

Não há alteração de schema, API, fixture ou fluxo de persistência.

## 6. Dependências, ondas e paralelismo

```text
T-01
```

| Onda | Tarefas | Pode executar em paralelo? | Gate para iniciar | Ordem de integração |
| --- | --- | --- | --- | --- |
| 1 | T-01 | não necessário | Decisões D-01 a D-04 confirmadas | T-01 |

### Matriz global de responsabilidade de arquivos

| Caminho/padrão | Tarefa dona | Exclusivo na onda? | Regra |
| --- | --- | --- | --- |
| `scripts/seed_financial.py` | T-01 | sim | Único arquivo de produto editável |
| `evidence/T-01.md` | T-01 | sim | Evidência sanitizada; não é produto/teste |
| Todo o restante do repositório | nenhuma | sim | Proibido editar |

## 7. Tarefas

### T-01 — Uniformizar todas as datas persistidas pelo seed em 2026

**Estado:** `ready`
**Onda:** 1
**Objetivo:** Todas as chamadas `datetime(...)` usadas como dados de domínio no
seed declaram o ano 2026, sem qualquer outra mudança funcional ou de dados.

**Dependências e pré-condições:**

- Decisões D-01 a D-04 confirmadas.
- Orquestrador deve mover a tarefa de `ready` para `in_progress` antes da
  execução.
- Developer deve conferir o diff preexistente do seed antes de editar e
  preservá-lo.

**Escopo:**

- Substituir o primeiro argumento 2025 ou 2027 por 2026 em todas as chamadas
  `datetime(...)` que compõem assinaturas, metas e transações do seed.
- Inspecionar todas as chamadas `datetime(...)` do arquivo após a mudança.
- Criar apenas o relatório documental `evidence/T-01.md`.

**Fora de escopo:**

- Qualquer edição fora de `scripts/seed_financial.py` e `evidence/T-01.md`.
- Executar seed, banco, Docker, Alembic ou testes que dependam de serviço real.
- Criar/editar testes e fixtures.
- Alterar qualquer argumento posterior ao ano ou qualquer outro campo.

**Responsabilidade de arquivos:**

- Exclusivos: `scripts/seed_financial.py`, `evidence/T-01.md`.
- Compartilhados: nenhum.
- Proibidos: `app/**`, `alembic/**`, `docker-compose.yml`, `.env*`,
  `app/tests/**` e qualquer outro arquivo não listado como exclusivo.

**Passos de implementação:**

1. Registrar no relatório a lista/contagem inicial de chamadas `datetime` por
   ano e conferir alterações preexistentes no seed.
2. Fazer substituição estritamente mecânica do argumento de ano 2025/2027 para
   2026, sem reformatar ou modificar outras linhas.
3. Inspecionar por AST todas as chamadas `datetime(...)` com primeiro argumento
   inteiro e provar que ele é 2026.
4. Revisar o diff palavra por palavra para confirmar que somente anos foram
   alterados.
5. Executar compilação e Ruff focados; não executar o seed.

**Critérios de aceite:**

- AC-01: Dado `scripts/seed_financial.py`, quando todas as chamadas
  `datetime(...)` com ano literal são enumeradas, então 100% têm primeiro
  argumento igual a 2026.
- AC-02: Para cada data convertida, os argumentos de mês, dia, hora e demais
  componentes são idênticos ao baseline.
- AC-03: O diff de produto contém alterações somente em
  `scripts/seed_financial.py` e cada hunk troca exclusivamente `2025` ou `2027`
  por `2026` no primeiro argumento de `datetime(...)`.
- AC-04: O seed compila e passa no Ruff focado.
- AC-05: Nenhum seed, banco, migração, Docker ou serviço real é executado.

**Cenários de teste:**

| ID | Nível | Cenário | Preparação | Ação | Resultado esperado | Prova de AC |
| --- | --- | --- | --- | --- | --- | --- |
| TS-01 | inspeção AST | uniformidade do ano | Parsear o seed sem importá-lo | Enumerar chamadas `datetime` com ano literal | Todas têm ano 2026; contagem registrada | AC-01 |
| TS-02 | inspeção de diff | preservação dos demais dados | Capturar diff do seed | Revisar pares removido/adicionado | Única diferença por data é o ano | AC-02, AC-03 |
| TS-03 | estático | sintaxe do seed | Arquivo alterado | Executar `py_compile` | Código 0 | AC-04 |
| TS-04 | estático | qualidade focada | Arquivo alterado | Executar Ruff somente no seed | Código 0 | AC-04 |
| TS-05 | segurança operacional | nenhuma persistência | Revisar comandos/evidência | Conferir execução | Nenhum comando mutante de DB/seed aparece | AC-05 |

**Comandos de verificação:**

```bash
rg -n 'datetime\((2025|2027),' scripts/seed_financial.py
rg -n 'datetime\(2026,' scripts/seed_financial.py
UV_CACHE_DIR=/tmp/financial-os-uv-cache uv run python -m py_compile scripts/seed_financial.py
UV_CACHE_DIR=/tmp/financial-os-uv-cache uv run ruff check scripts/seed_financial.py
git diff --word-diff=porcelain -- scripts/seed_financial.py
git status --short
```

Para AC-01, o Developer deve executar inspeção AST somente leitura que enumere
os primeiros argumentos inteiros das chamadas `datetime`; ela pode ser
executada por `uv run python -c` sem criar arquivos.

**Evidências esperadas:**

- relatório: `evidence/T-01.md`;
- contagens de `datetime` por ano antes/depois;
- saída resumida da inspeção AST, compilação, Ruff e status;
- diff sanitizado demonstrando alteração exclusiva dos anos.

**Paralelismo e integração:**

- Pode executar com: nenhuma tarefa que edite o seed.
- Não pode executar com: qualquer trabalho concorrente em
  `scripts/seed_financial.py`.
- Gate pós-integração: AC-01 a AC-05 comprovados no relatório.

**Riscos e rollback/mitigação:**

- Alterar ano em texto/nome legítimo → restringir edição ao primeiro argumento
  de `datetime(...)`.
- Alteração acidental de mês/dia/outro campo → revisão por word diff contra o
  baseline.
- Execução destrutiva do seed → comandos de aceite não importam nem chamam
  `seed()`; reconstrução permanece com o usuário.
- Alterações preexistentes no seed → preservar e registrar; nunca usar checkout
  ou reset destrutivo.

**Itens relacionados:** Q-01, V-01.

## 8. Estratégia de integração

1. Orquestrador libera T-01 para exatamente um Developer.
2. Developer altera somente o seed e produz `evidence/T-01.md`.
3. Orquestrador confere o diff contra AC-02/AC-03 e reproduz AST, compilação e
   Ruff.
4. Após aceite, o usuário reconstrói o banco fora desta entrega.

## 9. Matriz final de rastreabilidade

| Requisito da demanda | Tarefa | Critério de aceite | Cenário/prova |
| --- | --- | --- | --- |
| Todos os dados datados do seed em 2026 | T-01 | AC-01 | TS-01 |
| Preservar componentes e demais dados | T-01 | AC-02, AC-03 | TS-02 |
| Alterar apenas o seed | T-01 | AC-03 | TS-02, `git status` |
| Não operar o banco nem editar testes | T-01 | AC-05 | TS-05 |
| Seed válido estaticamente | T-01 | AC-04 | TS-03, TS-04 |

## 10. Dúvidas e descobertas abertas

| ID | Tipo | Estado | Descrição e evidência | Impacto e severidade | Responsável | Tarefas afetadas | Mitigação atual | Próxima ação | Histórico |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-01 | dúvida | resolvida | Escopo inicialmente ambíguo entre seed/API/banco | Alto | Solicitante | T-01 | Restrição exclusiva ao seed | Nenhuma | Respondida em 2026-07-29: somente `scripts/seed_financial.py`; banco será reconstruído pelo usuário |
| V-01 | vulnerabilidade | mitigada | O seed executa `DELETE` em várias tabelas e alerta não ser seguro para produção | Alto se executado no alvo errado | Usuário/Operação | fora da entrega | Nenhum comando executa/importa o seed | Usuário deve reconstruir apenas banco de desenvolvimento identificado | Detectada e registrada em 2026-07-29; refinamento excluiu operação de banco |
| O-01 | oportunidade | aceita fora do escopo | Routers ainda têm literais temporais de 2025 | Médio, mas explicitamente fora desta demanda | Backlog/Product Owner | backlog | Não editar arquivos proibidos | Criar demanda própria se houver impacto futuro | Escopo recusado pelo refinamento em 2026-07-29 |

## 11. Checklist final do Orquestrador

- [ ] T-01 está `accepted`.
- [ ] AC-01 a AC-05 possuem evidência reproduzível.
- [ ] Somente seed e evidência documental foram alterados pela execução.
- [ ] Nenhum banco, seed, migração, Docker ou serviço real foi executado.
- [ ] Nenhum teste/fixture foi criado ou editado.
- [ ] Itens externos permanecem explícitos e não foram incorporados ao escopo.
- [ ] O resultado observável foi verificado antes do arquivamento.
