from rest_framework import serializers
from ..domain.models.reservation import Reservation

class BookingSerializer(serializers.Serializer):
    """
    Serializer for incoming booking requests
    """
    num_individuals = serializers.IntegerField(
        min_value=1,
        help_text="The number of seats needed."
    )

class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a Reservation
    """
    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "table",
            "start_time",
            "end_time",
            "cost_amount",
            "cost_currency",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
