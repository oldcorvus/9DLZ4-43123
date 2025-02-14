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
