from abc import ABC, abstractmethod
from ...models.reservation import  Reservation, ReservationStatus
from ...models.price import Price
from ...models.table import Table

class ConcurrencyStrategy(ABC):
    """Base class for concurrency handling strategies"""
    
    
    @abstractmethod
    def create_reservation(
        self, 
        booking_service,  
        user,
        num_individuals,
        pricing_strategy
    ) -> Reservation:
        raise NotImplementedError("subclasses must impliment `create_reservation`")
    
    def create_reservation(self, user, table: Table, price: Price) -> Reservation:
        return Reservation.objects.create(
            user=user,
            table=table,
            cost_amount=price.amount,
            cost_currency=price.currency,
            status=ReservationStatus.CONFIRMED
        )
