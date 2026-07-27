
  # Streamable HTTP autenticado para o Financial OS MCP

  ## Resumo

  Disponibilizar o MCP por Streamable HTTP em /mcp, protegido por bearer token e publicado em desenvolvimento por Cloudflare Tunnel. O processo stdio continuará disponível como fallback. A integração seguirá
  o contrato de remote MCP da Responses API, que suporta Streamable HTTP e envia a credencial pelo campo authorization. Documentação oficial
  (https://developers.openai.com/api/docs/guides/tools-connectors-mcp)

  ## Alterações principais

  ### Servidor MCP

  - Reutilizar o catálogo atual de 13 tools em dois entrypoints:
      - financial-os-mcp: transporte stdio existente.
      - financial-os-mcp-http: Streamable HTTP stateless com respostas JSON em /mcp.

  - Adicionar configurações:
      - FINANCIAL_OS_MCP_HTTP_HOST, padrão 0.0.0.0.
      - FINANCIAL_OS_MCP_HTTP_PORT, padrão 8001.
      - FINANCIAL_OS_MCP_PUBLIC_URL.
      - FINANCIAL_OS_MCP_ENVIRONMENT, development ou production.
      - FINANCIAL_OS_MCP_AUTH_TOKEN ou arquivo Docker secret equivalente.

  - Exigir token opaco com pelo menos 32 bytes de entropia; validar Authorization: Bearer <token> com comparação em tempo constante.
  - Retornar 401 para token ausente ou inválido sem incluir a credencial em logs ou respostas.
  - Manter /healthz sem autenticação, retornando apenas o estado do processo; dados financeiros e protocolo MCP permanecem protegidos.
  - Habilitar proteção contra DNS rebinding e aceitar somente hosts derivados de MCP_PUBLIC_URL e endereços internos explicitamente configurados.
  - Em production, recusar inicialização se MCP_PUBLIC_URL não usar HTTPS. Publicação direta por HTTP/IP não será considerada válida.
  - Token único: documentar rotação coordenada entre MCP e cliente, admitindo interrupção breve.

  ### Containers e exposição

  - Tornar a imagem Docker capaz de iniciar API ou MCP, incluindo financial_os_mcp/ no build.
  - Fixar Python 3.13 em .python-version, versionar uv.lock e instalar dependências de forma travada para evitar nova resolução durante startup.
  - Completar o Compose com:
      - API na rede privada.
      - MCP HTTP consumindo http://api:8000.
      - Porta do MCP publicada apenas em 127.0.0.1:8001 para testes locais.
      - cloudflared em profile de desenvolvimento, encaminhando exclusivamente para http://mcp:8001.
      - Healthchecks e restart: unless-stopped.
      - Token montado como Docker secret; .env somente para desenvolvimento.

  - Usar Cloudflare Quick Tunnel apenas para testes. O fluxo documentado deverá obter a URL HTTPS dos logs, preencher MCP_PUBLIC_URL/URL do cliente e reiniciar o MCP quando necessário.
  - Na VPS, configurar MCP_PUBLIC_URL com o endereço definitivo. O deploy de produção ficará bloqueado até existir TLS — proxy, certificado direto ou túnel estável — mesmo que inicialmente os demais serviços
    sejam expostos diretamente por portas.

  ### Contrato com o cliente WhatsApp

  Fornecer implementação de referência para build_finance_mcp_tool():

  {
      "type": "mcp",
      "server_label": "financial_os",
      "server_description": "Consulta dados financeiros familiares no Financial OS.",
      "server_url": FINANCE_MCP_SERVER_URL,
      "authorization": FINANCE_MCP_AUTH_TOKEN,
      "allowed_tools": [...as 13 tools somente leitura...],
      "require_approval": "never",
  }

  - Validar URL e token no startup do cliente; configuração incompleta não deve desabilitar silenciosamente as tools.
  - Enviar o token bruto em authorization, sem prefixo Bearer, conforme o contrato da Responses API.
  - Nunca registrar o dicionário completo da tool ou headers.
  - Manter require_approval="never" apenas enquanto o catálogo for integralmente somente leitura.
  - Documentar tratamento de mcp_list_tools, mcp_call.error e indisponibilidade do MCP para impedir respostas financeiras inventadas.
  - A alteração concreta do cliente WhatsApp fica fora deste repositório; serão entregues contrato, exemplo e variáveis necessárias.

  ## Testes e aceite

  - Testes de configuração para token ausente/fraco, secrets por arquivo e rejeição de URL HTTP em produção.
  - Testes HTTP MCP:
      - /healthz acessível sem token.
      - /mcp retorna 401 sem token ou com token incorreto.
      - Handshake, tools/list e chamada de check_api_health funcionam com token correto.
      - Catálogo continua com 13 tools e nenhuma operação de escrita.
      - API indisponível produz erro MCP estruturado, sem vazar token.

  - Teste de integração com cliente Streamable HTTP do SDK, comprovando structured output.
  - Smoke test Compose: API saudável, MCP saudável e Cloudflare encaminhando somente o MCP.
  - Validação manual pela Responses API:
      - mcp_list_tools contém as 13 tools.
      - Pergunta de health gera mcp_call e retorna healthy.
      - Token inválido impede descoberta e execução.

  - Executar suíte completa em Python 3.13, Ruff e MyPy nos arquivos alterados, preservando os débitos globais existentes.

  ## Premissas

  - Desenvolvimento usa Cloudflare Quick Tunnel e bearer token.
  - Produção será numa VPS, mas não será liberada sem HTTPS.
  - O MCP e a API permanecem em rede privada; somente /mcp e /healthz serão expostos pelo túnel.
  - Não haverá OAuth, usuários, tenants ou tools de escrita nesta etapa.
  - stdio permanece compatível para Inspector e clientes locais.
  - Secure MCP Tunnel empresarial não faz parte desta implementação.
