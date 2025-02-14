from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from .seat import SeatCount


class Table(models.Model):
    """Root Entity for Table management"""
    class Meta:
        verbose_name = "Dining Table"
        verbose_name_plural = "Dining Tables"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, )
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(4), MaxValueValidator(10)]
    )
    is_booked = models.BooleanField(default=False)
    seat_price = models.PositiveBigIntegerField()
    version = models.IntegerField(default=0) 
    objects = TableManager() 
    

    def __str__(self):
        return f"{self.seats}- {self.seat_price} - {self.is_booked}"