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



class CancelReservationView(DestroyAPIView):
    """
    View to cancel a reservation and release its table
    """
    lookup_field = 'id'


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Reservation.objects.filter(user=user)
        return Reservation.objects.none()

    def destroy(self, request, *args, **kwargs):
        try:
            reservation = self.get_object()

            if reservation.status == ReservationStatus.CANCELLED:
                return Response(
                    {'error': 'Reservation already cancelled'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            booking_service = BookingService()
            result = booking_service.cancel_booking(reservation)

            if result:
                return Response(
                    {'message': 'Reservation cancelled successfully'},
                    status=status.HTTP_200_OK
                )
            raise ValueError("Failure in cancelling reservation")
        except Exception as e:
            return Response(
                    {'message': 'Reservation cancellation FAILED'},
                    status=status.HTTP_400_BAD_REQUEST
                )