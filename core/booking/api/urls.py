from django.urls import path
from .views import BookingCreateAPIView, CancelReservationView

urlpatterns = [
    path('bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('reservations/cancel/<uuid:id>/', CancelReservationView.as_view(), name='cancel_reservation'),

]
