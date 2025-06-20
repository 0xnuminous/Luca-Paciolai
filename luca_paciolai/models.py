from dataclasses import dataclass
from datetime import date
from typing import Optional

__all__ = ["Transaction", "TaxLot"]

@dataclass
class Transaction:
    """A double-entry journal entry."""
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


@dataclass
class TaxLot:
    """Represents an investment acquisition lot."""
    lot_id: str
    instrument: str
    quantity: float
    cost_basis_per_unit: float
    acquisition_date: date
