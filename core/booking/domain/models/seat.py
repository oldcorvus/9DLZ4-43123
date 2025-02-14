from django.core.exceptions import ValidationError

class SeatCount:
    """Value Object representing validated seat count"""
    def __init__(self, count: int):
        if count < 1:
            raise ValidationError("Seat count must be positive")
        self.count = count
        
    def __eq__(self, other):
        return self.count == other.count