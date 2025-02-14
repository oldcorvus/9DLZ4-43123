from typing import List, Tuple
from decimal import Decimal

from .base import BasePricingStrategy

from ...models.table import Table
from ...models.price import Price
from ...models.seat import SeatCount

class CheapestTableStrategy(BasePricingStrategy):
    def _adjust_seat_count(self, num_individuals: int, all_tables: List[Table]) -> int:

        valid_sizes = sorted({table.seats for table in all_tables})

        if num_individuals % 2 == 0:
            return num_individuals

        if num_individuals in valid_sizes:
            return num_individuals

        adjusted = num_individuals + 1
        if adjusted in valid_sizes:
            return adjusted

        next_even_size = next(
            (size for size in valid_sizes if size >= adjusted and size % 2 == 0),
            None
        )
        if next_even_size is not None:
            return next_even_size

        # Fallback: return the largest available table size
        return valid_sizes[-1]
