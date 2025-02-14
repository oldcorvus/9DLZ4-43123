from django.db import transaction

from ...models.table import Table
from .base import ConcurrencyStrategy

class NormalConcurrencyStrategy(ConcurrencyStrategy):
    """Handles reservations under normal load with database-level locking"""
    
    def create_reservation(self, user, num_individuals, pricing_strategy):
        with transaction.atomic():
            tables = Table.objects.select_for_update(skip_locked=True).find_available(num_individuals)
            if not tables:
                raise ValueError("No tables available")

            table, price = pricing_strategy.calculate(num_individuals, tables)
            reservation = self.create_reservation(user, table, num_individuals, price)
            table.mark_as_booked()
            table.save()
            return reservation