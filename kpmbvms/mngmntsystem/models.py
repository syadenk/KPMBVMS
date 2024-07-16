from django.db import models
from django.db import models
from django.utils import timezone

def current_time():
    return timezone.now().time()

class Admin(models.Model):
    userName = models.CharField(primary_key=True, max_length=8)
    password = models.TextField(max_length=128)
    fullName = models.TextField(max_length=128)
    
class User(models.Model):
    userName=models.CharField(primary_key=True, max_length=16)
    phoneNum=models.CharField(max_length=10)
    role=models.CharField(max_length=10)
    fullName=models.TextField(max_length=128)
    password=models.TextField(max_length=128)
    
class Vehicle(models.Model):
    vehicleID=models.CharField(primary_key=True, max_length=4)
    vehicleType=models.TextField(max_length=128)
    brand=models.TextField(max_length=128)
    capacity=models.IntegerField()
    plateNum=models.TextField(max_length=25)

class Driver(models.Model):
    driverID=models.CharField(primary_key=True, max_length=4)
    fullName=models.TextField(max_length=128)
    phoneNum=models.TextField(max_length=10)
    
class Booking(models.Model):
    bookingID=models.CharField(primary_key=True, max_length=4)
    userName=models.ForeignKey('User', on_delete=models.CASCADE)
    vehicleID=models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    driverID=models.ForeignKey('Driver', on_delete=models.CASCADE, null=True)
    bookingDate=models.DateField()
    bookingTime=models.TimeField(default=current_time)
    purpose=models.TextField(max_length=256)
    bookingStatus=models.TextField(max_length=8, default="Pending")
    
class Maintenance(models.Model):
    maintenanceID=models.CharField(primary_key=True, max_length=4)
    vehicleID=models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    maintenanceDate=models.DateField()
    availableDate=models.DateField()
    maintenanceReason=models.TextField()