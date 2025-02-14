from typing import List, Tuple
from decimal import Decimal

from .base import BasePricingStrategy

from ...models.table import Table
from ...models.price import Price
from ...models.seat import SeatCount

class CheapestTableStrategy(BasePricingStrategy):
    def calculate(self, num_individuals: SeatCount ,  
                available_tables: List[Table]) -> Tuple[Table, Price]:
        if num_individuals.count < 1:
            raise ValueError("At least 1 individual required")

        required_seats = self._adjust_seat_count(num_individuals.count, available_tables)

        price_options = []
        for table in available_tables:
            if table.seats < required_seats:
                continue
                
            if required_seats == table.seats:
                table_price = (table.seats - 1) * table.seat_price
            else:
                table_price = required_seats * table.seat_price
                
            price_options.append((table, table_price))
        
        if not price_options:
            raise ValueError("No suitable tables available")
        
        cheapest_option = min(price_options, key=lambda x: x[1])
        
        return (cheapest_option[0], Price(amount=cheapest_option[1]))

    def _adjust_seat_count(self, num_individuals: int, all_tables: List[Table]) -> int:
        valid_sizes = sorted({table.seats for table in all_tables})

        if num_individuals in valid_sizes:
            return num_individuals

        # If the number is even find the smallest table >= num_individuals
        if num_individuals % 2 == 0:
            next_available_size = next(
                (size for size in valid_sizes if size >= num_individuals),
                None
            )
            if next_available_size is not None:
                return next_available_size

        # For odd numbers round up to the next even number
        adjusted = num_individuals + 1
        if adjusted in valid_sizes:
            return adjusted

        # Find the smallest even table size >= adjusted
        next_even_size = next(
            (size for size in valid_sizes if size >= adjusted and size % 2 == 0),
            None
        )
        if next_even_size is not None:
            return next_even_size

        # Fallback: return the largest available table size
        return valid_sizes[-1]