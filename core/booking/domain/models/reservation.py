from django.db import models
import uuid
from django.conf import settings

from django.core.exceptions import ValidationError
from .time import ReservationTime
from .price import Price
from .table import Table

class ReservationStatus(models.TextChoices):
    PENDING = 'PND', 'Pending'
    CONFIRMED = 'CFM', 'Confirmed'
    CANCELLED = 'CNL', 'Cancelled'

class Reservation(models.Model):
    """Aggregate Root for Reservation management"""
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='reservations'
    )
    table = models.ForeignKey(
        'Table',
        on_delete=models.PROTECT,
        related_name='reservations'
    )
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    cost_amount = models.DecimalField(max_digits=8, decimal_places=2)
    cost_currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(
        max_length=3,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PENDING
    )
    version = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def reservation_time(self) -> ReservationTime:
        """Get as value object"""
        return ReservationTime(
            start=self.start_time,
            end=self.end_time
        )

    @reservation_time.setter
    def reservation_time(self, value: ReservationTime):
        """Set from value object"""
        self.start_time = value.start
        self.end_time = value.end

    @property
    def price(self) -> Price:
        """Get as value object"""
        return Price(
            amount=self.cost_amount,
            currency=self.cost_currency
        )

    @price.setter
    def price(self, value: Price):
        """Set from value object"""
        self.cost_amount = value.amount
        self.cost_currency = value.currency


    def clean(self):
        """Business rule validation"""
        try:
            price_obj = self.price  
            
            if self.status == ReservationStatus.CONFIRMED and not price_obj.amount > 0:
                raise ValidationError("Confirmed reservations must have positive price")
                
        except ValueError as e:
            raise ValidationError(str(e)) from e

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name="end_after_start"
            ),
            models.CheckConstraint(
                check=models.Q(cost_amount__gt=0),
                name="positive_price"
            )
        ]