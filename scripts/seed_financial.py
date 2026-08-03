"""Seed script to populate initial financial domain data.

Run with: `python scripts/seed_financial.py`

This seed populates realistic mock data to match frontend-data/*.ts mocks
so that dashboard endpoints and other APIs return expected values for tests.
"""

from datetime import datetime
from decimal import Decimal

from app.core.database import Base, SessionLocal, engine
from app.modules.accounts import models as acc_models
from app.modules.assets import models as asset_models
from app.modules.budgets import models as budget_models
from app.modules.categories import models as cat_models
from app.modules.credit_cards import models as card_models
from app.modules.goals import models as goal_models
from app.modules.investments import models as inv_models
from app.modules.loans import models as loan_models
from app.modules.owners import models as owner_models
from app.modules.settings import models as settings_models  # noqa: F401
from app.modules.subscriptions import models as sub_models
from app.modules.transactions import models as tx_models


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Clear existing data (simple, not cascade-safe for production)
        from sqlalchemy import text

        db.execute(text("DELETE FROM owner_credit_cards"))
        db.execute(text("DELETE FROM owner_accounts"))
        db.execute(text("DELETE FROM owners"))
        db.execute(text("DELETE FROM transactions"))
        db.execute(text("DELETE FROM credit_cards"))
        db.execute(text("DELETE FROM investments"))
        db.execute(text("DELETE FROM assets"))
        db.execute(text("DELETE FROM loans"))
        db.execute(text("DELETE FROM subscriptions"))
        db.execute(text("DELETE FROM goals"))
        db.execute(text("DELETE FROM budgets"))
        db.execute(text("DELETE FROM subcategories"))
        db.execute(text("DELETE FROM categories"))
        db.execute(text("DELETE FROM accounts"))
        db.commit()

        # ---------- Categories (with subcategories) ----------
        cats = [
            (
                "Moradia",
                "home",
                "expense",
                ["Aluguel", "Contas", "Financiamento", "Reparos"],
            ),
            (
                "Alimentação",
                "utensils",
                "expense",
                ["Supermercado", "Restaurante", "Delivery"],
            ),
            (
                "Transporte",
                "car",
                "expense",
                ["Combustível", "App", "Transporte público", "Estacionamento"],
            ),
            ("Lazer", "gamepad", "expense", ["Hobbies", "Viagem", "Eventos"]),
            (
                "Saúde",
                "heartbeat",
                "expense",
                ["Farmácia", "Consultas", "Fitness"],
            ),
            (
                "Assinaturas",
                "repeat",
                "expense",
                ["Streaming", "Música", "Software", "Armazenamento"],
            ),
            ("Renda", "wallet", "income", ["Salário", "Freelance", "Dividendos"]),
            ("Eletrônicos", "tv", "expense", ["Computador", "Celular", "Acessórios"]),
            (
                "Financeiro",
                "piggy-bank",
                "expense",
                ["Cartão de crédito", "Taxas", "Investimentos"],
            ),
        ]

        category_objs = {}
        for name, icon, ctype, subs in cats:
            c = cat_models.Category(name=name, icon=icon, type=ctype)
            c.subcategories = [cat_models.Subcategory(name=s) for s in subs]
            db.add(c)
            category_objs[name] = c
        db.commit()

        # ---------- Budgets ----------
        budgets = [
            ("Moradia", Decimal("4500.00")),
            ("Alimentação", Decimal("2000.00")),
            ("Transporte", Decimal("1200.00")),
            ("Lazer", Decimal("800.00")),
            ("Saúde", Decimal("900.00")),
            ("Assinaturas", Decimal("350.00")),
        ]
        db.add_all(
            budget_models.Budget(
                category_id=category_objs[category_name].id,
                month=7,
                year=2026,
                planned_amount=planned_amount,
            )
            for category_name, planned_amount in budgets
        )
        db.commit()

        # ---------- Accounts ----------
        accounts = [
            (
                "Conta Corrente",
                "Local Bank",
                "checking",
                Decimal("15420.15"),
                Decimal("15420.15"),
            ),
            (
                "Poupança de alta rentabilidade",
                "Local Bank",
                "savings",
                Decimal("22960.40"),
                Decimal("22960.40"),
            ),
            (
                "Conta Corretora",
                "Corretora X",
                "investment",
                Decimal("148320.90"),
                Decimal("148320.90"),
            ),
            (
                "Reserva de Emergência",
                "Local Bank",
                "savings",
                Decimal("32000.00"),
                Decimal("32000.00"),
            ),
        ]

        account_objs = {}
        for name, inst, atype, init_bal, cur_bal in accounts:
            a = acc_models.Account(
                name=name,
                institution=inst,
                type=atype.lower(),
                initial_balance=init_bal,
                current_balance=cur_bal,
                is_active=True,
            )
            db.add(a)
            account_objs[name] = a
        db.commit()

        # ---------- Credit Cards ----------
        cc1 = card_models.CreditCard(
            name="Cartão Platinum",
            issuer="Black Bank",
            last_four="4821",
            limit=Decimal("25000.00"),
            closing_day=22,
            due_day=30,
            active=True,
        )
        cc2 = card_models.CreditCard(
            name="Cartão Gold",
            issuer="Neon",
            last_four="1092",
            limit=Decimal("8000.00"),
            closing_day=18,
            due_day=26,
            active=True,
        )
        db.add_all([cc1, cc2])
        db.commit()

        # ---------- Owner ----------
        owner_phone = "7197038298"
        owner = owner_models.Owner(phone=owner_phone)
        owner.account_links = [
            owner_models.OwnerAccount(
                account_id=account.id,
                is_default=name == "Conta Corrente",
            )
            for name, account in account_objs.items()
        ]
        owner.credit_card_links = [
            owner_models.OwnerCreditCard(
                credit_card_id=card.id,
                is_default=card.name == "Cartão Platinum",
            )
            for card in (cc1, cc2)
        ]
        db.add(owner)
        db.commit()

        # ---------- Subscriptions ----------
        subs = [
            (
                "Netflix",
                "Streaming",
                Decimal("55.90"),
                datetime(2026, 7, 24),
                "Cartão Platinum",
                True,
            ),
            (
                "Spotify Família",
                "Música",
                Decimal("34.90"),
                datetime(2026, 7, 28),
                "Cartão Gold",
                True,
            ),
            (
                "Amazon Prime",
                "Streaming",
                Decimal("14.90"),
                datetime(2026, 8, 3),
                "Cartão Platinum",
                True,
            ),
            (
                "ChatGPT Plus",
                "Software",
                Decimal("110.00"),
                datetime(2026, 8, 6),
                "Cartão Platinum",
                True,
            ),
            (
                "Xbox Game Pass",
                "Games",
                Decimal("44.90"),
                datetime(2026, 8, 12),
                "Cartão Gold",
                False,
            ),
            (
                "iCloud 200GB",
                "Armazenamento",
                Decimal("12.90"),
                datetime(2026, 8, 15),
                "Cartão Platinum",
                True,
            ),
            (
                "Notion",
                "Software",
                Decimal("42.00"),
                datetime(2026, 8, 19),
                "Cartão Platinum",
                True,
            ),
        ]
        for name, cat, monthly, renew, method, active in subs:
            s = sub_models.Subscription(
                name=name,
                category=cat,
                monthly_value=monthly,
                renewal_date=renew,
                payment_method=method,
                active=active,
            )
            db.add(s)
        db.commit()

        # ---------- Goals ----------
        goals = [
            (
                "Reserva de Emergência",
                Decimal("45000.00"),
                Decimal("32000.00"),
                datetime(2026, 12, 31),
                False,
            ),
            (
                "Viagem ao Japão",
                Decimal("22000.00"),
                Decimal("8400.00"),
                datetime(2026, 4, 30),
                False,
            ),
            (
                "Computador Novo",
                Decimal("12000.00"),
                Decimal("6800.00"),
                datetime(2026, 9, 30),
                False,
            ),
            (
                "Carro Novo",
                Decimal("90000.00"),
                Decimal("12000.00"),
                datetime(2027, 6, 30),
                False,
            ),
            (
                "Reforma de casa",
                Decimal("30000.00"),
                Decimal("4500.00"),
                datetime(2026, 3, 31),
                False,
            ),
        ]
        for name, target, current, deadline, completed in goals:
            g = goal_models.Goal(
                name=name,
                target_amount=target,
                current_amount=current,
                deadline=deadline,
                completed=completed,
            )
            db.add(g)
        db.commit()

        # ---------- Assets ----------
        assets = [
            (
                "Apartamento — Vila Mariana",
                "real_estate",
                Decimal("540000.00"),
                Decimal("612000.00"),
            ),
            ("Honda Civic 2022", "vehicle", Decimal("148000.00"), Decimal("129000.00")),
            ("Yamaha MT-07", "motorcycle", Decimal("42000.00"), Decimal("39500.00")),
            ("Coleção de Board Games", "collectible", Decimal("14200.00"), Decimal("17800.00")),
            ("Eletrônicos", "electronics", Decimal("22000.00"), Decimal("15400.00")),
            ("Reserva em caixa", "cash", Decimal("15420.15"), Decimal("15420.15")),
            ("Reserva de Emergência", "cash", Decimal("32000.00"), Decimal("32000.00")),
        ]
        for name, atype, purchase, current in assets:
            a = asset_models.Asset(
                name=name, asset_type=atype, purchase_value=purchase, current_value=current
            )
            db.add(a)
        db.commit()

        # ---------- Investments ----------
        portfolio = [
            ("VALE3", "stock", Decimal("120"), Decimal("62.10"), Decimal("68.40")),
            ("PETR4", "stock", Decimal("200"), Decimal("32.40"), Decimal("38.50")),
            ("ITSA4", "stock", Decimal("800"), Decimal("9.80"), Decimal("11.20")),
            ("IVVB11", "etf", Decimal("50"), Decimal("260.40"), Decimal("320.10")),
            ("BOVA11", "etf", Decimal("80"), Decimal("112.40"), Decimal("118.20")),
            (
                "TESOURO IPCA 2035",
                "treasury_bond",
                Decimal("1"),
                Decimal("4200.00"),
                Decimal("4820.00"),
            ),
            ("BTC", "cryptocurrency", Decimal("0.12"), Decimal("210000.00"), Decimal("340000.00")),
            ("ETH", "cryptocurrency", Decimal("1.4"), Decimal("12800.00"), Decimal("18400.00")),
        ]
        for ticker, atype, qty, avg, cur in portfolio:
            inv = inv_models.Investment(
                ticker=ticker,
                asset_type=atype,
                quantity=qty,
                average_price=avg,
                current_price=cur,
                broker="Corretora X",
            )
            db.add(inv)
        db.commit()

        # ---------- Loans ----------
        loans = [
            (
                "Financiamento imobiliário",
                "mortgage",
                Decimal("420000.00"),
                Decimal("268400.00"),
                Decimal("9.4"),
                360,
                92,
            ),
            (
                "Financiamento Honda Civic",
                "vehicle",
                Decimal("78000.00"),
                Decimal("31200.00"),
                Decimal("12.1"),
                60,
                34,
            ),
            (
                "Empréstimo pessoal",
                "personal",
                Decimal("12000.00"),
                Decimal("4400.00"),
                Decimal("18.9"),
                24,
                15,
            ),
        ]
        for name, ltype, original, current, rate, total, paid in loans:
            ln = loan_models.Loan(
                name=name,
                loan_type=ltype,
                original_amount=original,
                current_balance=current,
                interest_rate=rate,
                total_installments=total,
                paid_installments=paid,
            )
            db.add(ln)
        db.commit()

        # ---------- Transactions (match frontend mocks) ----------
        # Helper to lookup ids
        def cat_id(name):
            return db.query(cat_models.Category).filter(cat_models.Category.name == name).first().id

        def sub_id(cat_name, sub_name):
            cat = db.query(cat_models.Category).filter(cat_models.Category.name == cat_name).first()
            return (
                db.query(cat_models.Subcategory)
                .filter(
                    cat_models.Subcategory.category_id == cat.id,
                    cat_models.Subcategory.name == sub_name,
                )
                .first()
                .id
            )

        def acc_id(name):
            return db.query(acc_models.Account).filter(acc_models.Account.name == name).first().id

        txs = [
            # id t1
            (
                "Conta Corrente",
                "Renda",
                "Salário",
                "Salário — Acme Corp",
                Decimal("18500.00"),
                "income",
                "bank_transfer",
                "cleared",
                datetime(2026, 7, 14),
            ),
            (
                "Conta Corrente",
                "Alimentação",
                "Supermercado",
                "Mercado — Hortifruti",
                Decimal("284.60"),
                "expense",
                "debit_card",
                "cleared",
                datetime(2026, 7, 14),
            ),
            (
                "Conta Corrente",
                "Transporte",
                "App",
                "Uber para o aeroporto",
                Decimal("68.40"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 13),
                1,
                1,
                None,
                "Cartão Platinum",
            ),
            (
                "Conta Corrente",
                "Lazer",
                "Hobbies",
                "Board Game — Ark Nova",
                Decimal("549.90"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 12),
                1,
                6,
                3,
                "Cartão Gold",
            ),
            (
                "Conta Corrente",
                "Moradia",
                "Aluguel",
                "Aluguel — Julho",
                Decimal("3200.00"),
                "expense",
                "bank_transfer",
                "cleared",
                datetime(2026, 7, 11),
            ),
            (
                "Conta Corrente",
                "Assinaturas",
                "Streaming",
                "Netflix",
                Decimal("55.90"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 10),
                1,
                1,
                1,
                "Cartão Platinum",
            ),
            (
                "Conta Corretora",
                "Renda",
                "Dividendos",
                "Dividendo — VALE3",
                Decimal("214.32"),
                "income",
                "bank_transfer",
                "cleared",
                datetime(2026, 7, 9),
            ),
            (
                "Conta Corrente",
                "Alimentação",
                "Restaurante",
                "Restaurante — Fasano",
                Decimal("412.00"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 8),
                1,
                1,
                1,
                "Cartão Platinum",
            ),
            (
                "Conta Corrente",
                "Moradia",
                "Contas",
                "Conta de luz",
                Decimal("218.75"),
                "expense",
                "automatic_debit",
                "cleared",
                datetime(2026, 7, 7),
            ),
            (
                "Conta Corrente",
                "Transporte",
                "Combustível",
                "Combustível",
                Decimal("320.00"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 6),
                1,
                1,
                1,
                "Cartão Gold",
            ),
            (
                "Conta Corrente",
                "Renda",
                "Freelance",
                "Freela — Projeto UI",
                Decimal("3200.00"),
                "income",
                "bank_transfer",
                "cleared",
                datetime(2026, 7, 5),
            ),
            (
                "Conta Corrente",
                "Saúde",
                "Farmácia",
                "Farmácia",
                Decimal("142.80"),
                "expense",
                "debit_card",
                "cleared",
                datetime(2026, 7, 4),
            ),
            (
                "Conta Corrente",
                "Assinaturas",
                "Música",
                "Spotify Família",
                Decimal("34.90"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 3),
                1,
                1,
                1,
                "Cartão Gold",
            ),
            (
                "Conta Corrente",
                "Eletrônicos",
                "Computador",
                'Monitor Novo — LG 27"',
                Decimal("2199.00"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 2),
                2,
                10,
                2,
                "Cartão Platinum",
            ),
            (
                "Conta Corrente",
                "Saúde",
                "Fitness",
                "Academia — mensal",
                Decimal("159.90"),
                "expense",
                "credit_card",
                "cleared",
                datetime(2026, 7, 1),
                1,
                1,
                1,
                "Cartão Gold",
            ),
            (
                "Conta Corrente",
                "Moradia",
                "Financiamento",
                "Parcela do financiamento imobiliário",
                Decimal("2450.00"),
                "expense",
                "bank_transfer",
                "scheduled",
                datetime(2026, 7, 16),
            ),
            (
                "Conta Corrente",
                "Financeiro",
                "Cartão de crédito",
                "Fatura Cartão — Platinum",
                Decimal("3210.40"),
                "expense",
                "bank_transfer",
                "scheduled",
                datetime(2026, 7, 18),
            ),
        ]

        for item in txs:
            # Unpack considering optional fields
            account_name = item[0]
            category_name = item[1]
            sub_name = item[2]
            desc = item[3]
            amount = item[4]
            ttype = item[5]
            method = item[6]
            status = item[7]
            tdate = item[8]
            installment_number = None
            installment_total = None
            card_name = None
            if len(item) >= 11:
                installment_number = item[9]
                installment_total = item[10]
            if len(item) >= 12:
                # optional explicit installment count when placed differently
                installment_total = item[10]
            if len(item) >= 13:
                card_name = item[12]

            tx = tx_models.Transaction(
                account_id=None if method == "credit_card" else acc_id(account_name),
                category_id=cat_id(category_name),
                subcategory_id=sub_id(category_name, sub_name),
                description=desc,
                amount=amount,
                transaction_type=ttype,
                payment_method=method,
                status=status,
                transaction_date=tdate,
                installment_number=installment_number,
                installment_total=installment_total,
            )
            if card_name:
                cc = (
                    db.query(card_models.CreditCard)
                    .filter(card_models.CreditCard.name == card_name)
                    .first()
                )
                if cc:
                    tx.credit_card_id = cc.id
            db.add(tx)
        db.commit()

        print("Seed data created successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
