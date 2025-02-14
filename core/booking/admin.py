from django.contrib import admin
from .domain.models.reservation import Reservation
from .domain.models.table import Table
# Register your models here.
admin.site.register(Reservation)
admin.site.register(Table)