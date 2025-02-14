from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from .seat import SeatCount


class TableQuerySet(models.QuerySet):
    def find_available(self, seats_needed: SeatCount):
        return self.filter(
            seats__gte=seats_needed.count,
            is_booked=False
        )
class TableManager(models.Manager):
    def get_queryset(self):
        return TableQuerySet(self.model, using=self._db)
    
    def find_available(self, seats_needed: SeatCount):
        return self.get_queryset().find_available(seats_needed)
    
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
    
    def mark_as_booked(self):
        """To book table"""
        if self.is_booked:
            raise ValidationError("Table already booked")
        self.is_booked = True
        self.version += 1
        
    def release_table(self):
        """To release table"""
        if not self.is_booked:
            raise ValidationError("Table not currently booked")
        self.is_booked = False
        self.version += 1

    def __str__(self):
        return f"Table {self.id}: {self.seats} seats at {self.seat_price} ({'Booked' if self.is_booked else 'Available'})"