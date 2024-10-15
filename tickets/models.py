from django.db import models

# Create your models here.

# Model for Routes
class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.origin} to {self.destination}"

# Model for Vehicles
class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('bus', 'Bus'),
        ('microbus', 'Microbus'),
        ('taxi', 'Taxi'),
    ]
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    name = models.CharField(max_length=100, unique=True)  # Added vehicle name field
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    seats_total = models.IntegerField()

    def __str__(self):
        return f"{self.vehicle_type} - {self.name} for route {self.route}"

# Model for Seats
class Seat(models.Model):
    vehicle = models.ForeignKey(Vehicle, related_name='seats', on_delete=models.CASCADE)
    seat_id = models.CharField(max_length=5)  # Changed to CharField for seat ID
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_id} in {self.vehicle}"


# Model for Bookings
class Booking(models.Model):
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user_name} for {self.seat.seat_id} in {self.vehicle.name}"
