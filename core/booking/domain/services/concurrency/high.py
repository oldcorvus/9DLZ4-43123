from django.db import transaction
from django.core.cache import cache

from ...models.table import Table
from .base import ConcurrencyStrategy

class HighConcurrencyStrategy(ConcurrencyStrategy):
    """Handles reservations under high load with Redis locks"""

    LOCK_TIMEOUT = 300 

    def create_reservation(self,user, num_individuals, pricing_strategy):
        redis_client = cache.client.get_client()
        lock_key = f"table:{num_individuals.count}:lock"
        
        if not redis_client.set(
            lock_key, 
            user.id, 
            nx=True, 
            ex=self.LOCK_TIMEOUT  
        ):
            raise ValueError("High traffic – please try again later")

        try:
            with transaction.atomic():
                tables = Table.objects.find_available(num_individuals)
                if not tables:
                    raise ValueError("No tables available")

                table, price = pricing_strategy.calculate(num_individuals, tables)
                reservation = self._create_reservation(user, table, price)
                table.mark_as_booked()
                table.save()
                return reservation
        finally:
            redis_client.delete(lock_key) 