from rest_framework import serializers
from .models import Route, Vehicle, Seat, Booking

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'origin', 'destination']

class VehicleSerializer(serializers.ModelSerializer):
    route = RouteSerializer()

    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_type', 'route', 'departure_date', 'departure_time', 'seats_total']

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_id', 'is_booked']

class SeatBookingSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=20)
    vehicle_name = serializers.CharField(max_length=100)
    seat_ids = serializers.ListField(child=serializers.CharField(max_length=5))

    def validate(self, data):
        # Ensure the vehicle exists
        vehicle = Vehicle.objects.filter(name=data['vehicle_name']).first()
        if not vehicle:
            raise serializers.ValidationError("The vehicle with this name does not exist.")

        # Ensure all seat IDs are valid and belong to the vehicle
        seats = Seat.objects.filter(vehicle=vehicle, seat_id__in=data['seat_ids'], is_booked=False)
        if len(seats) != len(data['seat_ids']):
            raise serializers.ValidationError("One or more seats are invalid or already booked.")
        
        # Pass the validated vehicle and seats to be used later
        data['vehicle'] = vehicle
        data['seats'] = seats
        return data
