from django.db import transaction
from django.db.models import F
from ..models.seat import SeatCount
from ..models.table import Table
from ..models.reservation import Reservation, ReservationStatus
from .pricing.base import BasePricingStrategy
from .concurrency.base import ConcurrencyStrategy
from .concurrency.high import HighConcurrencyStrategy
from .concurrency.normal import NormalConcurrencyStrategy

class BookingService:
  
    LAST_TABLES_THRESHOLD = 5

    def __init__(self):
        self.strategies = {
            "normal": NormalConcurrencyStrategy(),
            "high": HighConcurrencyStrategy()
        }

    def create_booking(
        self, 
        user, 
        num_individuals: SeatCount, 
        pricing_strategy: BasePricingStrategy
    ) -> Reservation:
        """Selects and executes the appropriate concurrency strategy"""
        strategy = self._select_concurrency_strategy()
        return strategy.create_reservation(
            self, 
            user,
            num_individuals,
            pricing_strategy
        )

    def _select_concurrency_strategy(self) -> ConcurrencyStrategy:
        if self._should_use_redis():
            return self.strategies["high"]
        return self.strategies["normal"]

    def _should_use_redis(self) -> bool:
        return Table.objects.filter(is_booked=False).count() <= self.LAST_TABLES_THRESHOLD




    def cancel_booking(self, reservation: Reservation):
        with transaction.atomic():

            reservation.status =  ReservationStatus.CANCELLED
            reservation.save()
            
            table = reservation.table
            try:
                table.release_table()
                table.save()
                return reservation
            except Exception as e:
                 raise ValueError("failure in canceling reservation")
                
 