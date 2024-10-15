# from django.urls import path
# from . import views

# urlpatterns = [
#     path('routes/', views.RouteListView.as_view(), name='route-list'),
#     path('vehicles/<int:route_id>/<str:departure_date>/', views.vehicle_list, name='vehicle-list'),
#     path('seats/<int:vehicle_id>/', views.seat_list, name='seat-list'),
#     path('book-seats/', views.book_seats, name='book-seats'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    # List all unique places (origins and destinations)
    path('places/', views.list_places, name='list-places'),
    
    # List destinations by origin
    path('routes/<str:origin>/destinations/', views.destinations_by_origin, name='destinations-by-origin'),
    
   # List vehicles by route, date, and vehicle type
    path('routes/<str:origin>/<str:destination>/vehicles/<str:date>/<str:vehicle_type>/', 
         views.vehicles_by_route_date_type, name='vehicles-by-route-date-type'),
    
    # List all seats for a vehicle
    path('vehicles/<str:vehicle_name>/seats/', views.seats_for_vehicle, name='seats-for-vehicle'),

    # book seat
    path('book-seats/', views.book_seats, name='book-seats'),
]
