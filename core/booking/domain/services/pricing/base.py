from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Tuple
from ...models.table import Table
from ...models.price import Price

class BasePricingStrategy(ABC):
    @abstractmethod
    def calculate(
        self,
        num_individuals: int,
        available_tables: List[Table],
    ) -> Tuple[Table, Price]:
        raise NotImplementedError("sub classes must impliment `calculate` method")