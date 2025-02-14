from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import BookingSerializer, ReservationSerializer
from ..domain.services.booking import BookingService
from ..domain.models.seat import SeatCount
from ..domain.models.reservation import Reservation, ReservationStatus
from ..domain.services.pricing.seat_count import CheapestTableStrategy

class BookingCreateAPIView(CreateAPIView):
    """
    API endpoint for creating a booking
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        num_individuals_value = serializer.validated_data["num_individuals"]
        try:
            seat_count = SeatCount(num_individuals_value)
        
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        booking_service = BookingService()
        pricing_strategy = CheapestTableStrategy()
        try:
            reservation = booking_service.create_booking(request.user, seat_count, pricing_strategy)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        reservation_data = ReservationSerializer(reservation).data
        return Response(reservation_data, status=status.HTTP_201_CREATED)

