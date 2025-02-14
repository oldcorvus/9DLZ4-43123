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
