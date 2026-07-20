from fastapi import APIRouter
from app.shared.responses.api import SuccessResponse

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/insights", response_model=SuccessResponse)
def get_ai_insights():
    data = [
        {
            "kind": "warning",
            "title": "Orçamento de alimentação excedido",
            "body": "Você já usou 115% do orçamento de Alimentação. Considere reduzir refeições fora esta semana.",
            "icon": "alert"
        },
        {
            "kind": "recommendation",
            "title": "Mover dinheiro parado para a poupança",
            "body": "R$ 8.420 estão parados na conta corrente há 40 dias. Mover para a poupança renderia ~R$ 55/mês.",
            "icon": "sparkles"
        },
        {
            "kind": "prediction",
            "title": "Saldo projetado para o final do mês",
            "body": "Com base nas contas agendadas, você fechará julho com cerca de R$ 39.600.",
            "icon": "trending"
        },
        {
            "kind": "anomaly",
            "title": "Cobrança fora do padrão detectada",
            "body": "R$ 549,90 em Board Games é 3,4x seu gasto típico mensal nesta categoria.",
            "icon": "search"
        },
        {
            "kind": "opportunity",
            "title": "Cancelar assinatura ociosa",
            "body": "Xbox Game Pass não é usado há 62 dias — cancelar economiza R$ 44,90/mês.",
            "icon": "scissors"
        },
        {
            "kind": "invest",
            "title": "Sugestão de rebalanceamento",
            "body": "Cripto representa agora 18% da carteira vs. alvo de 9%. Considere reduzir BTC em ~R$ 3.200.",
            "icon": "chart"
        }
    ]
    return {"success": True, "data": data}


@router.get("/conversations", response_model=SuccessResponse)
def get_ai_conversations():
    data = [
        {"id": "conv1", "title": "Posso comprar um notebook novo?", "date": "Hoje"},
        {"id": "conv2", "title": "Revisão do orçamento de board games", "date": "Ontem"},
        {"id": "conv3", "title": "Assinaturas para cancelar", "date": "12/Jul"},
        {"id": "conv4", "title": "Planejamento viagem Japão", "date": "08/Jul"},
        {"id": "conv5", "title": "Projeção de aposentadoria", "date": "04/Jul"}
    ]
    return {"success": True, "data": data}


@router.get("/suggestions", response_model=SuccessResponse)
def get_ai_suggestions():
    data = [
        "Posso fazer uma compra de R$600 em 10x?",
        "Quanto gastei em restaurantes este mês?",
        "Quanto gastei em board games este ano?",
        "Mostre meus maiores gastos deste ano.",
        "Quanto vou ter disponível depois de pagar o financiamento?",
        "Quais assinaturas eu deveria cancelar?",
        "Quanto economizei em relação ao mês passado?"
    ]
    return {"success": True, "data": data}
