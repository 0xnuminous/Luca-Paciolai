from datetime import date
from luca_paciolai.ledger import create_session, add_transaction, list_accounts
from luca_paciolai.models import Transaction


def test_list_accounts_returns_unique_names():
    session = create_session("sqlite:///:memory:")
    tx1 = Transaction(
        date=date.today(),
        description="Coffee",
        debit="Expenses:Coffee",
        credit="Assets:Cash",
        amount=5.0,
        currency="USD",
    )
    tx2 = Transaction(
        date=date.today(),
        description="Salary",
        debit="Assets:Cash",
        credit="Income:Salary",
        amount=100.0,
        currency="USD",
    )
    add_transaction(session, tx1)
    add_transaction(session, tx2)
    accounts = list_accounts(session)
    assert accounts == ["Assets:Cash", "Expenses:Coffee", "Income:Salary"]
