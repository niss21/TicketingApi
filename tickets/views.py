from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework import status
from .models import Route, Vehicle, Seat, Booking
from .serializers import RouteSerializer, VehicleSerializer, SeatSerializer, SeatBookingSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# show all the places
@api_view(['GET'])
def list_places(request):
    # Fetch unique places from both the origin and destination
    origins = Route.objects.values_list('origin', flat=True).distinct()
    destinations = Route.objects.values_list('destination', flat=True).distinct()

    # Combine both origin and destination, and remove duplicates
    places = set(origins).union(set(destinations))

    return Response({"places": list(places)})

# show all the destination places from a origin
@api_view(['GET'])
def destinations_by_origin(request, origin):
    routes = Route.objects.filter(origin=origin)
    destinations = routes.values_list('destination', flat=True)
    return Response({"origin": origin, "destinations": list(destinations)})

# list all the vehicles.
from datetime import datetime
@api_view(['GET'])
def vehicles_by_route_date_type(request, origin, destination, date, vehicle_type):
    # Find the route
    route = Route.objects.filter(origin=origin, destination=destination).first()
    if not route:
        return Response({"error": "Route not found"}, status=404)

    # Validate the departure date
    try:
        departure_date = datetime.strptime(date, '%Y-%m-%d').date()  # Convert the date to a proper format
    except ValueError:
        return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

    # Fetch vehicles matching the route, date, and vehicle type
    vehicles = Vehicle.objects.filter(route=route, departure_date=departure_date, vehicle_type=vehicle_type)

    if not vehicles.exists():
        return Response({"error": "No vehicles found for this route, date, and vehicle type"}, status=404)

    # Prepare the vehicle data with their departure times
    vehicle_data = [
        {"vehicle_name": vehicle.name, "departure_time": vehicle.departure_time} 
        for vehicle in vehicles
    ]

    return Response({
        "route": f"{origin} to {destination}",
        "departure_date": departure_date,
        "vehicle_type": vehicle_type,
        "vehicles": vehicle_data
    })


# list all the seats
@api_view(['GET'])
def seats_for_vehicle(request, vehicle_name):
    vehicle = Vehicle.objects.filter(name=vehicle_name).first()
    if not vehicle:
        return Response({"error": "Vehicle not found"}, status=404)
    
    seats = Seat.objects.filter(vehicle=vehicle)
    data = [{"seat_id": seat.seat_id, "is_booked": seat.is_booked} for seat in seats]
    
    return Response({
        "vehicle_name": vehicle.name,
        "seats": data
    })


# Booking a seat
@api_view(['POST'])
def book_seats(request):
    serializer = SeatBookingSerializer(data=request.data)
    
    if serializer.is_valid():
        # Retrieve validated data
        user_name = serializer.validated_data['user_name']
        phone_number = serializer.validated_data['phone_number']
        vehicle = serializer.validated_data['vehicle']
        seats = serializer.validated_data['seats']

        # Create bookings and mark seats as booked
        for seat in seats:
            seat.is_booked = True
            seat.save()
            
            # Create a Booking record
            Booking.objects.create(
                user_name=user_name,
                phone_number=phone_number,
                vehicle=vehicle,
                seat=seat
            )

        return Response({"message": "Seats booked successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # List available routes
# class RouteListView(generics.ListAPIView):
#     queryset = Route.objects.all()
#     serializer_class = RouteSerializer

# # List vehicles for a given route and departure date
# @api_view(['GET'])
# def vehicle_list(request, route_id, departure_date):
#     vehicles = Vehicle.objects.filter(route_id=route_id, departure_date=departure_date)
#     serializer = VehicleSerializer(vehicles, many=True)
#     return Response(serializer.data)

# # List available seats for a selected vehicle
# @api_view(['GET'])
# def seat_list(request, vehicle_id):
#     seats = Seat.objects.filter(vehicle_id=vehicle_id, is_booked=False)
#     serializer = SeatSerializer(seats, many=True)
#     return Response(serializer.data)


