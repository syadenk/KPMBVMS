from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Admin, Booking, Driver, Vehicle, Maintenance
from django.urls import reverse
from urllib.parse import urlencode
from datetime import date


def welcomepage(request):
    return render(request, 'mngmntsystem/welcomepage.html')

def homepage(request):
    username = request.session.get('username')
    password = request.session.get('password')
    print(username)
    print(password)

    user_credentials = User.objects.filter(userName=username).values('userName', 'password','phoneNum','role','fullName').first()
    booking_credentials = Booking.objects.filter(userName=username)
    if user_credentials:
        username_ver = user_credentials.get("userName")
        password_ver = user_credentials.get("password")

        if username_ver == username and password_ver == password:
            context = {
                'user_credentials': user_credentials,
                'booking_credentials':booking_credentials
            }
            return render(request, 'mngmntsystem/homepage.html', context)
    
    error = "Error acquiring login info from database. Must be wrong password or username. Please login again."
    context = {
        'error': error,
    }
    
    return render(request, 'mngmntsystem/homepage.html', context)

def logout(request):
    return HttpResponseRedirect(reverse('welcomepage'))
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        request.session['username'] = username
        request.session['password'] = password

        # Retrieve the user with the provided username
        user_credentials = User.objects.filter(userName=username).first()
        if user_credentials:
            username_ver = user_credentials.userName
            password_ver = user_credentials.password
            if username_ver == username and password_ver == password:
                return redirect('homepage')
            else:
                # Authentication failed
                error_message = "Invalid username or password"
                return render(request, 'mngmntsystem/login.html', {'error_message': error_message})

    return render(request, 'mngmntsystem/login.html')


def register(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        phone_num = request.POST['phoneNum']
        role = request.POST['role']
            
        User.objects.create(
            userName=username,
            password=password,
            fullName=full_name,
            phoneNum=phone_num,
            role=role
        )
        return redirect('login',)
    else:
        return render(request,'mngmntsystem/register.html')
    
def booking(request):
    username = request.session.get('username', None)
    request.session['username'] = username
    maintenance_vehicle_ids = Maintenance.objects.values_list('vehicleID', flat=True)
    available_vehicles = Vehicle.objects.exclude(vehicleID__in=maintenance_vehicle_ids)
    current_date = date.today()
    Maintenance.objects.filter(availableDate=current_date).delete()
    maintenance = Maintenance.objects.all()
    print(available_vehicles)
    vehicles=Vehicle.objects.all()
    user=User.objects.filter(userName=username).values('userName').first()
    username_ver = user.get("userName")
    booking=Booking.objects.all()
    list_bookingID=[]
    if booking:
        for i in booking:
            x=i.bookingID
            list_bookingID.append(x)
        highest_value=max(list_bookingID)
        letter_part= highest_value[0]
        numeric_part=int(highest_value[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
    else:
        template="B000"
        letter_part= template[0]
        numeric_part=int(template[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
        new_string = new_string[0] if isinstance(new_string, tuple) else new_string
    
    if request.method=='POST':
        bookingid=new_string
        username=username_ver
        vehicleid=request.POST['vehicleid']
        bookingdate=request.POST['bookingdate']
        Purpose=request.POST['purpose']
        
        Booking.objects.create(
            bookingID=bookingid,
            userName=User.objects.get(userName=username),
            vehicleID=Vehicle.objects.get(vehicleID=vehicleid),
            bookingDate=bookingdate,
            purpose=Purpose
        )
        print(type(new_string))
        print(type(bookingid))
        message_done = "Booking has been sent! Please wait for approval."
        context = {
            'message_done ': message_done,
            'vehicles': vehicles,
            'maintenance':maintenance,
            'available_vehicles': available_vehicles, 
        }
        return render(request, 'mngmntsystem/booking.html', context)
    dict = {
        'vehicles': vehicles,
        'available_vehicles': available_vehicles, 
    }
    return render(request, 'mngmntsystem/booking.html', dict)

def update(request, bookingID):
    updateBooking=Booking.objects.get(bookingID=bookingID)
    maintenance_vehicle_ids = Maintenance.objects.values_list('vehicleID', flat=True)
    available_vehicles = Vehicle.objects.exclude(vehicleID__in=maintenance_vehicle_ids)
    dict={
        'updateBooking':updateBooking,
        'vehicles':available_vehicles,
        
    }
    return render(request, 'mngmntsystem/update.html', dict)

def update_booking_data(request, bookingID):
    bookingdate=request.POST['bookingdate']
    reason=request.POST['reason']
    vehicleid=request.POST['vehicleID']
    data=Booking.objects.get(bookingID=bookingID)
    data.bookingDate=bookingdate
    data.purpose=reason
    data.vehicleID=Vehicle.objects.get(vehicleID=vehicleid)
    data.save()
    return HttpResponseRedirect(reverse('homepage'))

def delete_booking_data(request, bookingID):
    deleteBooking=Booking.objects.get(bookingID=bookingID)
    deleteBooking.delete()
    return HttpResponseRedirect(reverse('homepage'))

def maintenance(request):
    maintenance=Maintenance.objects.all()
    current_date = date.today()
    Maintenance.objects.filter(availableDate=current_date).delete()
    maintenance = Maintenance.objects.all()
    context={
        'maintenance':maintenance
    }
    return render(request, 'mngmntsystem/maintenance.html', context)

def vehicles(request):
    if request.POST:
        Brand=request.POST['brand']
        vehicle=Vehicle.objects.filter(brand=Brand)
        dict={
            'vehicle':vehicle 
        }
        return render(request, 'mngmntsystem/vehicles.html', dict)
    return render(request, 'mngmntsystem/vehicles.html')

def driver(request):
    driver=Driver.objects.all()
    context={
        'driver':driver
    }
    return render(request, 'mngmntsystem/driver.html', context)

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        
        admin_credentials = Admin.objects.filter(userName=username).values('userName', 'password').first()
        if admin_credentials:
            username_ver = admin_credentials.get("userName")
            password_ver = admin_credentials.get("password")

            if username_ver == username and password_ver == password:
                request.session['username'] = username
                request.session['password'] = password
                return redirect('admin_homepage')
            else:
                error_message = "Invalid username or password"
                context = {
                    'error_message': error_message,
                }
                return render(request, 'mngmntsystem/admin_login.html', context)

    return render(request, 'mngmntsystem/admin_login.html')  # Render the login page for GET requests

def admin_homepage(request):
    username = request.session.get('username', None)
    return render(request, 'mngmntsystem/admin_homepage.html')

def admin_booking(request):
    username = request.session.get('username', None)
    booking=Booking.objects.all()
    driver=Driver.objects.all()
    notify="There is no bookings right now."
    context={
        'booking':booking,
        'driver':driver,
        'notify':notify,
    }
    if request.method == 'POST':
        bookingid= request.POST['bookingid']
        bookingstatus= request.POST['bookingstatus']
        driverid= request.POST['driverid']
        
        data=Booking.objects.get(bookingID=bookingid)
        if bookingstatus=='Approved': 
            data.bookingStatus=bookingstatus
            data.driverID=Driver.objects.get(driverID=driverid)
        else:
            data.bookingStatus=bookingstatus
        data.save()
        return render(request, 'mngmntsystem/admin_booking.html', context)
    
    return render(request, 'mngmntsystem/admin_booking.html', context)

def admin_delete_booking(request):
    if request.method=='POST':
        bookingid=request.POST['bookingid']
        data=Booking.objects.get(bookingID=bookingid)
        data.delete()
        return HttpResponseRedirect(reverse('admin_booking'))
    
def admin_driver(request):
    if request.method=='POST':
        driverid=request.POST['driverid']
        fullname=request.POST['fullname']
        phonenum=request.POST['phonenum']
        Driver.objects.create(
            driverID=driverid,
            fullName=fullname,
            phoneNum=phonenum
        )
        return HttpResponseRedirect(reverse('admin_driver'))
    
    username = request.session.get('username', None)
    driver=Driver.objects.all()
    list_driverID=[]
    if driver:
        for i in driver:
            x=i.driverID
            list_driverID.append(x)
        highest_value=max(list_driverID)
        letter_part= highest_value[0]
        numeric_part=int(highest_value[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
    else:
        template="D000"
        letter_part= template[0]
        numeric_part=int(template[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
        
        
    context={
        'driver':driver,
        'new_string':new_string,
    }
    return render(request, 'mngmntsystem/admin_driver.html', context)

def admin_driver_delete(request):
    if request.method=='POST':
        driverid=request.POST['driverid']
        data=Driver.objects.get(driverID=driverid)
        data.delete()
        return HttpResponseRedirect(reverse('admin_driver'))
    
def admin_vehicle(request):
    if request.method=='POST':
        vehicleid=request.POST['vehicleid']
        vehicletype=request.POST['vehicletype']
        Brand=request.POST['brand']
        Capacity=request.POST['capacity']
        Platenum=request.POST['platenum']
        Vehicle.objects.create(
            vehicleID=vehicleid,
            vehicleType=vehicletype,
            brand=Brand,
            capacity=Capacity,
            plateNum=Platenum,
        )
        return HttpResponseRedirect(reverse('admin_vehicle'))
    
    username = request.session.get('username', None)
    vehicle=Vehicle.objects.all()
    list_vehicleID=[]
    if vehicle:
        for i in vehicle:
            x=i.vehicleID
            list_vehicleID.append(x)
        highest_value=max(list_vehicleID)
        letter_part= highest_value[0]
        numeric_part=int(highest_value[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
    else:
        template="V000"
        letter_part= template[0]
        numeric_part=int(template[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
        
        
    context={
        'vehicle':vehicle,
        'new_string':new_string,
    }
    return render(request, 'mngmntsystem/admin_vehicle.html', context)

def admin_vehicle_delete(request):
    if request.method=='POST':
        vehicleid=request.POST['vehicleid']
        data=Vehicle.objects.get(vehicleID=vehicleid)
        data.delete()
        return HttpResponseRedirect(reverse('admin_vehicle'))
    
def admin_vehicle_update(request):
    if request.method=='POST':
        vehicleid=request.POST['vehicleid']
        Capacity=request.POST['capacity']
        Platenum=request.POST['platenum']
        data=Vehicle.objects.get(vehicleID=vehicleid)
        data.capacity=Capacity
        data.plateNum=Platenum
        data.save()
        return HttpResponseRedirect(reverse('admin_vehicle'))
    
def admin_maintenance(request):
    if request.method=='POST':
        maintenanceid=request.POST['maintenanceid']
        vehicleid=request.POST['vehicleid']
        maintenancedate=request.POST['maintenancedate']
        availabledate=request.POST['availabledate']
        maintenancereason=request.POST['maintenancereason']
        Maintenance.objects.create(
            maintenanceID=maintenanceid,
            vehicleID=Vehicle.objects.get(vehicleID=vehicleid),
            maintenanceDate=maintenancedate,
            availableDate=availabledate,
            maintenanceReason=maintenancereason,
        )
        return HttpResponseRedirect(reverse('admin_maintenance'))
    
    username = request.session.get('username', None)
    maintenance=Maintenance.objects.all()
    vehicle=Vehicle.objects.all()
    list_maintenanceID=[]
    if maintenance:
        for i in maintenance:
            x=i.maintenanceID
            list_maintenanceID.append(x)
        highest_value=max(list_maintenanceID)
        letter_part= highest_value[0]
        numeric_part=int(highest_value[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
    else:
        template="M000"
        letter_part= template[0]
        numeric_part=int(template[1:])
        new_numeric_part= numeric_part + 1
        new_string=f"{letter_part}{new_numeric_part:03d}"
        
        
    context={
        'maintenance':maintenance,
        'vehicle':vehicle,
        'new_string':new_string,
    }
    return render(request, 'mngmntsystem/admin_maintenance.html', context)

def admin_maintenance_delete(request):
    if request.method=='POST':
        maintenanceid=request.POST['maintenanceid']
        data=Maintenance.objects.get(maintenanceID=maintenanceid)
        data.delete()
        return HttpResponseRedirect(reverse('admin_maintenance'))