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
    price: Optional[float] = None
    lot_id: Optional[str] = None


class TaxLot(SQLModel, table=True):  # type: ignore[call-arg]
    """Represents an investment acquisition lot."""
    id: Optional[int] = Field(default=None, primary_key=True)
    lot_id: str
    instrument: str
    quantity: float
    cost_basis_per_unit: float
    acquisition_date: date
