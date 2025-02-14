from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator

class Price(BaseModel):
    """Value Object for monetary values"""
    amount: Decimal
    currency: str = "USD"
    
    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("Price must be positive")
        return v 
