from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Route, Vehicle, Seat, Booking

# Registering the Route model
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination')
    search_fields = ('origin', 'destination')

# Register the Vehicle model
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'route', 'departure_date', 'departure_time', 'seats_total')
    search_fields = ('vehicle_type',)
    list_filter = ('vehicle_type', 'departure_date')

# Register the Seat model
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'seat_id', 'is_booked')
    list_filter = ('is_booked',)

# Register the Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'phone_number', 'seat', 'vehicle', 'booking_time')
    search_fields = ('user_name', 'phone_number')
    list_filter = ('vehicle', 'seat')
