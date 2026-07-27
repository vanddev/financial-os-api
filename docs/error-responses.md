# Respostas de erro

Todas as respostas de erro da API usam o mesmo envelope:

```json
{
  "success": false,
  "code": "validation_error",
  "message": "Request validation failed",
  "details": [
    {
      "field": "body.amount",
      "message": "Input should be greater than 0",
      "type": "greater_than",
      "context": {
        "gt": 0
      }
    }
  ],
  "request_id": "19cc2c4e-33d4-4f20-af8d-1b360cd8de44"
}
```

## Campos

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `success` | boolean | Sempre `false` em respostas de erro. |
| `code` | string | Código estável para tratamento programático. |
| `message` | string | Mensagem legível; pode ser específica do endpoint. |
| `details` | objeto, lista ou `null` | Contexto adicional. Erros de validação usam uma lista por campo. |
| `request_id` | string ou `null` | Identificador para correlação com logs e suporte. |

O cliente deve tomar decisões com base em `status` e `code`, não comparando o texto de
`message`.

## Status e códigos

| HTTP | Código padrão | Uso |
| --- | --- | --- |
| 400 | `bad_request` ou `invalid_json` | Sintaxe ou JSON malformado. |
| 401 | `unauthorized` | Credenciais ausentes ou inválidas. Pode incluir `WWW-Authenticate`. |
| 403 | `forbidden` | Identidade válida, mas sem autorização. |
| 404 | `not_found` | Rota ou recurso inexistente. |
| 409 | `conflict` | Conflito de estado, idempotência ou integridade. |
| 422 | `validation_error` | Parâmetros ou conteúdo semanticamente inválidos. |
| 429 | `rate_limit_exceeded` | Limite de requisições excedido. Pode incluir `Retry-After`. |
| 5xx | `internal_server_error` | Falha inesperada; detalhes internos não são expostos. |

Os contratos também aparecem automaticamente em cada operação no OpenAPI, disponível
em `/docs` e `/openapi.json`.
