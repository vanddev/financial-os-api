"""Normalize finite domain values to English.

Revision ID: normalize_domain_values
Revises: add_transaction_idempotency
"""

from alembic import op

revision = "normalize_domain_values"
down_revision = "add_transaction_idempotency"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE accounts
        SET type = CASE lower(type)
            WHEN 'corrente' THEN 'checking'
            WHEN 'poupança' THEN 'savings'
            WHEN 'poupanca' THEN 'savings'
            WHEN 'investimento' THEN 'investment'
            WHEN 'dinheiro' THEN 'cash'
            ELSE type
        END
        """
    )
    op.execute(
        """
        UPDATE categories
        SET type = CASE lower(type)
            WHEN 'receita' THEN 'income'
            WHEN 'despesa' THEN 'expense'
            ELSE type
        END
        """
    )
    op.execute(
        """
        UPDATE transactions
        SET transaction_type = CASE lower(transaction_type)
            WHEN 'receita' THEN 'income'
            WHEN 'despesa' THEN 'expense'
            ELSE transaction_type
        END,
        payment_method = CASE lower(payment_method)
            WHEN 'dinheiro' THEN 'cash'
            WHEN 'débito' THEN 'debit_card'
            WHEN 'debito' THEN 'debit_card'
            WHEN 'crédito' THEN 'credit_card'
            WHEN 'credito' THEN 'credit_card'
            WHEN 'transferência' THEN 'bank_transfer'
            WHEN 'transferencia' THEN 'bank_transfer'
            WHEN 'débito automático' THEN 'automatic_debit'
            WHEN 'debito automatico' THEN 'automatic_debit'
            WHEN 'boleto' THEN 'bank_slip'
            WHEN 'corretora' THEN 'bank_transfer'
            WHEN 'brokerage' THEN 'bank_transfer'
            ELSE payment_method
        END,
        status = CASE lower(status)
            WHEN 'pendente' THEN 'pending'
            WHEN 'confirmada' THEN 'cleared'
            WHEN 'confirmado' THEN 'cleared'
            WHEN 'agendada' THEN 'scheduled'
            WHEN 'agendado' THEN 'scheduled'
            WHEN 'cancelada' THEN 'cancelled'
            WHEN 'cancelado' THEN 'cancelled'
            ELSE status
        END
        """
    )
    op.execute(
        """
        UPDATE assets
        SET asset_type = CASE lower(asset_type)
            WHEN 'imóvel' THEN 'real_estate'
            WHEN 'imovel' THEN 'real_estate'
            WHEN 'veículo' THEN 'vehicle'
            WHEN 'veiculo' THEN 'vehicle'
            WHEN 'motocicleta' THEN 'motorcycle'
            WHEN 'colecionável' THEN 'collectible'
            WHEN 'colecionavel' THEN 'collectible'
            WHEN 'eletrônicos' THEN 'electronics'
            WHEN 'eletronicos' THEN 'electronics'
            WHEN 'dinheiro' THEN 'cash'
            WHEN 'outros' THEN 'other'
            ELSE asset_type
        END
        """
    )
    op.execute(
        """
        UPDATE investments
        SET asset_type = CASE lower(asset_type)
            WHEN 'ação' THEN 'stock'
            WHEN 'acao' THEN 'stock'
            WHEN 'ações' THEN 'stock'
            WHEN 'acoes' THEN 'stock'
            WHEN 'tesouro' THEN 'treasury_bond'
            WHEN 'cripto' THEN 'cryptocurrency'
            WHEN 'renda fixa' THEN 'fixed_income'
            WHEN 'fundo' THEN 'fund'
            WHEN 'fundos' THEN 'fund'
            WHEN 'outros' THEN 'other'
            ELSE asset_type
        END
        """
    )
    op.execute(
        """
        UPDATE loans
        SET loan_type = CASE lower(loan_type)
            WHEN 'imobiliário' THEN 'mortgage'
            WHEN 'imobiliario' THEN 'mortgage'
            WHEN 'veicular' THEN 'vehicle'
            WHEN 'pessoal' THEN 'personal'
            WHEN 'consignado' THEN 'payroll'
            WHEN 'outros' THEN 'other'
            ELSE loan_type
        END
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE accounts
        SET type = CASE type
            WHEN 'checking' THEN 'corrente'
            WHEN 'savings' THEN 'poupança'
            WHEN 'investment' THEN 'investimento'
            WHEN 'cash' THEN 'dinheiro'
            ELSE type
        END
        """
    )
    op.execute(
        """
        UPDATE categories
        SET type = CASE type
            WHEN 'income' THEN 'receita'
            WHEN 'expense' THEN 'despesa'
            ELSE type
        END
        """
    )
    op.execute(
        """
        UPDATE transactions
        SET transaction_type = CASE transaction_type
            WHEN 'income' THEN 'receita'
            WHEN 'expense' THEN 'despesa'
            ELSE transaction_type
        END,
        payment_method = CASE payment_method
            WHEN 'cash' THEN 'dinheiro'
            WHEN 'debit_card' THEN 'débito'
            WHEN 'credit_card' THEN 'crédito'
            WHEN 'bank_transfer' THEN 'transferência'
            WHEN 'automatic_debit' THEN 'débito automático'
            WHEN 'bank_slip' THEN 'boleto'
            ELSE payment_method
        END,
        status = CASE status
            WHEN 'pending' THEN 'pendente'
            WHEN 'cleared' THEN 'confirmada'
            WHEN 'scheduled' THEN 'agendada'
            WHEN 'cancelled' THEN 'cancelada'
            ELSE status
        END
        """
    )
    op.execute(
        """
        UPDATE assets
        SET asset_type = CASE asset_type
            WHEN 'real_estate' THEN 'imóvel'
            WHEN 'vehicle' THEN 'veículo'
            WHEN 'motorcycle' THEN 'motocicleta'
            WHEN 'collectible' THEN 'colecionável'
            WHEN 'electronics' THEN 'eletrônicos'
            WHEN 'cash' THEN 'dinheiro'
            ELSE asset_type
        END
        """
    )
    op.execute(
        """
        UPDATE investments
        SET asset_type = CASE asset_type
            WHEN 'stock' THEN 'ação'
            WHEN 'treasury_bond' THEN 'tesouro'
            WHEN 'cryptocurrency' THEN 'cripto'
            WHEN 'fixed_income' THEN 'renda fixa'
            WHEN 'fund' THEN 'fundo'
            ELSE asset_type
        END
        """
    )
    op.execute(
        """
        UPDATE loans
        SET loan_type = CASE loan_type
            WHEN 'mortgage' THEN 'imobiliário'
            WHEN 'vehicle' THEN 'veicular'
            WHEN 'personal' THEN 'pessoal'
            WHEN 'payroll' THEN 'consignado'
            ELSE loan_type
        END
        """
    )
