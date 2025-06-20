from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel

__all__ = ["Transaction", "TaxLot"]

class Transaction(SQLModel, table=True):  # type: ignore[call-arg]
    """A double-entry journal entry."""
    id: Optional[int] = Field(default=None, primary_key=True)
    date: date
    description: str
    debit: str
    credit: str
    amount: float
    currency: str
    instrument: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    lot_id: Optional[str] = None
    fee_amount: Optional[float] = None
    fee_currency: Optional[str] = None
    fee_account: Optional[str] = None
    memo: Optional[str] = None
    reference_number: Optional[str] = None
    vendor: Optional[str] = None
    payment_method: Optional[str] = None
    tax_amount: Optional[float] = None
    tax_rate: Optional[float] = None
    reconciled: Optional[bool] = None


class TaxLot(SQLModel, table=True):  # type: ignore[call-arg]
    """Represents an investment acquisition lot."""
    id: Optional[int] = Field(default=None, primary_key=True)
    lot_id: str
    instrument: str
    quantity: float
    cost_basis_per_unit: float
    acquisition_date: date
