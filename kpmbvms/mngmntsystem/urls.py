from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcomepage, name='welcomepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('homepage/', views.homepage, name='homepage'),
    path('logout/', views.logout, name='logout'),  
    path('booking/', views.booking, name='booking'),
    path('homepage/update/<str:bookingID>', views.update, name='update'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('homepage/update/update_booking_data/<str:bookingID>', views.update_booking_data, name='update_booking_data'),
    path('homepage/delete_booking_data/<str:bookingID>', views.delete_booking_data, name='delete_booking_data'),
    path('maintenance/', views.maintenance, name='maintenance'),
    path('driver/', views.driver, name='driver'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_homepage/', views.admin_homepage, name='admin_homepage'),
    path('admin_booking/', views.admin_booking, name='admin_booking'),
    path('admin_delete_booking/', views.admin_delete_booking, name='admin_delete_booking'),
    path('admin_driver/', views.admin_driver, name='admin_driver'),
    path('admin_driver_delete/', views.admin_driver_delete, name='admin_driver_delete'),
    path('admin_vehicle/', views.admin_vehicle, name='admin_vehicle'),
    path('admin_vehicle_delete/', views.admin_vehicle_delete, name='admin_vehicle_delete'),
    path('admin_vehicle_update/', views.admin_vehicle_update, name='admin_vehicle_update'),
    path('admin_maintenance/', views.admin_maintenance, name='admin_maintenance'),
    path('admin_maintenance_delete/', views.admin_maintenance_delete, name='admin_maintenance_delete'),
    
       
]