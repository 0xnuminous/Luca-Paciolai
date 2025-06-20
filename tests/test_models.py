from datetime import date

from luca_paciolai.models import Transaction, TaxLot


def test_transaction_creation() -> None:
    tx = Transaction(
        date=date.today(),
        description="Coffee",
        debit="Expenses:Coffee",
        credit="Assets:Cash",
        amount=6.0,
        currency="USD",
        memo="morning run",
        fee_amount=0.5,
    )
    assert tx.amount == 6.0


def test_tax_lot_creation() -> None:
    lot = TaxLot(
        lot_id="abc123",
        instrument="BTC",
        quantity=0.5,
        cost_basis_per_unit=1000.0,
        acquisition_date=date.today(),
    )
    assert lot.instrument == "BTC"
