# Workflow reutilizável de planejamento e execução

Esta pasta define um protocolo portátil para demandas de software conduzidas
por agentes. Ela pode ser copiada para outro repositório junto com o trecho
"Agent Delivery Workflow" de `AGENTS.md`.

O princípio central é separar quem transforma a demanda em um plano de quem
altera o produto. O planejamento é um contrato executável: uma tarefa só pode
ser delegada quando outro agente consegue implementá-la e comprová-la sem
inventar escopo, contratos ou critérios de sucesso.

## Perfis

- `profiles/orchestrator.md`: recebe a demanda, aciona os perfis na ordem
  correta, controla dependências, conflitos e gates.
- `profiles/product-manager.md`: investiga o repositório e produz o plano
  detalhado. Não implementa a feature.
- `profiles/developer.md`: implementa uma tarefa liberada, cria os testes e
  registra evidências e decisões.

Cada agente deve ler primeiro `AGENTS.md`, este arquivo e seu próprio perfil.
Depois, deve ler o `handoff.md` ativo e apenas os contratos/fontes relevantes à
tarefa.

## Artefatos

| Artefato | Responsável | Finalidade |
| --- | --- | --- |
| `handoff.md` | Product Manager | Fonte de verdade temporária da demanda ativa |
| `docs/handoffs/<data>-<slug>.md` | Orquestrador | Registro imutável de uma demanda encerrada |
| `evidence/<task-id>.md` | Developer | Prova de implementação, testes, inspeções e pendências |
| `docs/adr/<id>-<slug>.md` | Developer | Decisão arquitetural relevante que surgiu na execução |
| código e testes | Developer | Entrega funcional da tarefa |

O diretório `evidence/` pode ser trocado no plano caso o projeto já tenha uma
convenção. Não incluir segredos, payloads reais, dados pessoais, logs completos
ou artefatos gerados pesados. Saída resumida de comandos é suficiente; a prova
principal deve ser reproduzível por comando e por teste versionado.

## Ciclo de vida do handoff

O `handoff.md` da raiz representa exatamente uma demanda ativa. Ele é um
artefato temporário de coordenação, não um documento cumulativo e não deve
existir entre demandas.

O ciclo obrigatório é:

```text
sem demanda ativa
  -> criar handoff.md a partir do template
  -> planejar e executar uma única demanda
  -> consolidar aceite e itens abertos
  -> arquivar em docs/handoffs/<data>-<slug>.md
  -> remover handoff.md da raiz
  -> sem demanda ativa
```

### Criação

1. Antes de criar um plano, o Orquestrador verifica se já existe
   `handoff.md`.
2. Se não existir, o Product Manager copia
   `.agents/templates/handoff.template.md`, atribui um novo ID de entrega e
   preserva a demanda original.
3. Se existir, o Orquestrador deve confirmar que o ID corresponde à demanda
   atual e que o estado não é terminal.
4. Um `handoff.md` de outra demanda, concluído ou com identidade ambígua nunca
   pode ser reaproveitado, sobrescrito ou reinterpretado. Ele deve ser
   arquivado corretamente antes da criação do novo plano.

### Uso durante a demanda

- Apenas a demanda identificada no cabeçalho pode alterar objetivo, tarefas e
  estados daquele handoff.
- Todo agente deve conferir ID, estado e fonte da demanda antes de usar o
  arquivo.
- Decisões, evidências e itens abertos devem ser consolidados continuamente;
  informação relevante não pode permanecer apenas na conversa.
- Planos arquivados podem ser consultados como histórico, mas nunca usados
  como fila de tarefas executáveis.

### Encerramento e arquivamento

Depois do gate de aceite final, o Orquestrador:

1. marca o plano com estado terminal `done` ou `cancelled`, conforme o
   resultado real;
2. registra data de encerramento, resumo do aceite, evidências e todas as
   dúvidas, dívidas técnicas, pendências de negócio, vulnerabilidades e
   oportunidades ainda abertas;
3. garante que cada item aberto tenha responsável, impacto, mitigação e
   próxima ação em backlog ou artefato persistente;
4. move o arquivo, preservando seu conteúdo, para
   `docs/handoffs/<AAAA-MM>-<slug-da-demanda>.md`;
5. verifica que não existe mais `handoff.md` na raiz.

O nome do arquivo arquivado deve ser único, estável e descritivo. Em caso de
colisão, usar o ID da entrega; nunca sobrescrever um histórico existente.

Após arquivado, o handoff é imutável. Correções factuais posteriores devem ser
feitas por adendo datado e identificado, sem reabrir tarefas nem alterar o
resultado histórico. Uma continuação, correção ou nova fase exige outra demanda
e um novo `handoff.md`, com referência explícita ao plano arquivado quando
aplicável.

### Gate contra reutilização indevida

Nenhuma tarefa pode receber `ready` ou ser entregue a um Developer quando:

- o handoff está em estado terminal;
- o ID ou a fonte da demanda não correspondem à solicitação atual;
- o arquivo foi copiado de um plano anterior sem novo ID e nova demanda
  original;
- existe outro handoff ativo;
- o caminho aponta para `docs/handoffs/`.

Se qualquer condição ocorrer, o Orquestrador interrompe a execução, arquiva ou
corrige o artefato e solicita novo planejamento. Não é permitido “reabrir só
uma tarefa” em um handoff concluído.

## Fluxo obrigatório

```text
demanda
  -> Orquestrador: TRIAGE
  -> Product Manager: PLANNING
  -> Orquestrador: PLAN_REVIEW
  -> Developer(es): EXECUTING
  -> Orquestrador: ACCEPTANCE
  -> DONE ou REPLAN
```

1. **TRIAGE:** o Orquestrador preserva a demanda original, identifica apenas
   restrições já explícitas e a entrega ao Product Manager.
2. **PLANNING:** o Product Manager inspeciona código, testes, documentação e
   contratos; cria ou atualiza `handoff.md` usando o template.
3. **PLAN_REVIEW:** o Orquestrador aplica o gate de prontidão. Lacunas voltam
   ao Product Manager; elas não são resolvidas pelo Developer.
4. **EXECUTING:** cada Developer recebe uma tarefa pronta e respeita sua
   propriedade de arquivos. Tarefas paralelas só começam quando o plano
   declara que não há dependência nem sobreposição.
5. **ACCEPTANCE:** o Orquestrador confronta a evidência com cada critério de
   aceite. Falha de implementação volta ao Developer; descoberta que muda
   escopo ou contrato volta para replanejamento.
6. **DONE:** todos os critérios estão comprovados, decisões estão registradas
   e nenhuma pendência bloqueante está escondida. O Orquestrador encerra e
   arquiva o handoff conforme o ciclo de vida acima.

## Estados

Use estes estados no plano:

- `draft`: ainda sendo detalhada pelo Product Manager;
- `blocked`: depende de decisão, contrato ou insumo nomeado;
- `ready`: passou pelo gate e pode ser executada;
- `in_progress`: atribuída a exatamente um Developer;
- `implemented`: código e testes concluídos, aguardando aceite;
- `accepted`: evidências conferidas pelo Orquestrador;
- `failed`: implementação não atende ao contrato e precisa de correção.
- `done`: demanda aceita e encerrada, pronta para arquivamento;
- `cancelled`: demanda encerrada sem entrega completa, com motivo, impacto e
  itens remanescentes registrados.

Somente o Product Manager move `draft` para `ready`; somente o Orquestrador
move `ready` para `in_progress` e `implemented` para `accepted`. O Developer
move sua tarefa de `in_progress` para `implemented` ou `blocked`. `done` e
`cancelled` são estados terminais da demanda, não estados reutilizáveis para
novas tarefas.

## Gate de prontidão da tarefa

Uma tarefa pode receber `ready` somente quando contém:

- ID estável, título, objetivo observável e motivação;
- dependências e pré-condições;
- escopo e fora de escopo;
- responsabilidade de arquivos sem colisão não coordenada;
- passos pequenos o bastante para uma entrega coesa;
- critérios de aceite objetivos e numerados;
- cenários de teste com sucesso, falha e bordas aplicáveis;
- comandos de verificação executáveis;
- estratégia de paralelismo e integração;
- riscos, contratos externos e perguntas bloqueantes;
- caminho esperado para a evidência.

Critérios vagos como "funcionar corretamente", "testar bem" ou "melhorar a
qualidade" não passam pelo gate.

## Regras de paralelismo

O Product Manager cria ondas de execução e uma tabela de propriedade de
arquivos. Duas tarefas podem rodar ao mesmo tempo apenas se:

1. todas as dependências de ambas estiverem aceitas;
2. não escreverem no mesmo arquivo, migração, snapshot ou fixture
   compartilhada;
3. não estabilizarem lados opostos de uma interface ainda indefinida;
4. a ordem de integração e o teste pós-integração estiverem definidos.

Arquivos compartilhados devem ter um único dono por onda. Trabalho documental
também conta como escrita e pode gerar conflito.

## Desvios durante a execução

- Correção local necessária e compatível com o aceite: o Developer implementa
  e registra na evidência.
- Decisão arquitetural relevante e dentro do objetivo: o Developer cria um
  ADR a partir do template e referencia-o na evidência.
- Mudança de requisito, contrato externo, responsabilidade de arquivos ou
  aceite: o Developer para a parte afetada, marca `blocked` e devolve ao
  Orquestrador para `REPLAN`.
- Falha preexistente não relacionada: registrar comando, sintoma e impacto;
  não ampliar silenciosamente o escopo.

## Como adotar em outro projeto

1. Copie `.agents/` para a raiz do repositório.
2. Acrescente `.agents/templates/AGENTS.snippet.md` ao `AGENTS.md` local,
   adaptando apenas convenções específicas do projeto.
3. Ajuste nomes de comandos, diretórios de evidência e ADR no template.
4. Copie `templates/handoff.template.md` para `handoff.md` somente quando
   iniciar uma nova demanda e não houver outro handoff ativo.
5. Preserve no topo do plano a demanda original e um identificador único da
   entrega.
6. Ao encerrar, arquive o plano em `docs/handoffs/` e remova o arquivo ativo da
   raiz antes de aceitar outra demanda.

O template é deliberadamente independente de linguagem, framework e provedor
de agentes.
