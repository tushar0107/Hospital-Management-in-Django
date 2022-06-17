from audioop import reverse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .models import Appointment, Doctor, Patient, Staff, User
from django.contrib.auth.models import Group
import requests
# Create your views here.


def home(request):
    return render(request,'hospital/home.html')

def register(request):
    return render(request,'hospital/doctor_register.html')

def doctor_after_login(request):
    appointments = Appointment.objects.all()
    user = request.user
    return render(request,'hospital/doctor_page.html', {'appointments':appointments,'user':user})


def staff_admin(request):
    if request.user.is_authenticated:
        patients = Patient.objects.all()
        return render(request, 'hospital/staff.html', {'patients':patients})
    else:
        return redirect('home')

#login for doctor
def doctor_login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        doctor = auth.authenticate(request,username=username,password=password)
        if doctor is not None:
            auth.login(request,doctor)
            messages.info(request,'logging in')
            return redirect('doctor_after_login')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('home')
    else:
        return render(request,'hospital/home.html')

def doctor_register(request):
    if request.method == 'POST':
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        department = request.POST.get('department')
        password = request.POST.get('pwd')

        if Doctor.objects.filter(mobile=mobile).exists():
            messages.info(request,'mobile exists!')
            print('mobile exists')
            return redirect('doctor_register')
        elif Doctor.objects.filter(email=email).exists():
            messages.info(request,'Email exists!')
            print('email exists')
            return redirect('doctor_register')
        else:
            doctor = Doctor.objects.create_user(firstname,lastname,email,mobile,
            address,department,password)
            #creating a DOCTOR group
            doctor.save()
            doctor_group = Group.objects.get_or_create(name='DOCTOR')
            doctor_group[0].user_set.add(doctor)
            login(request,doctor)
            messages.success(request,"Account Created!")
            print('account created')
            return redirect('home')
    else:
        return render(request,'hospital/home.html')


def staff_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        staff_type = request.POST.get('staff_type')
        password = request.POST.get('pwd')

        if Staff.objects.filter(mobile=mobile).exists():
            messages.info(request,'mobile exists!')
            print('mobile exists')
            return redirect('doctor_register')
        elif Doctor.objects.filter(email=email).exists():
            messages.info(request,'Email exists!')
            print('email exists')
            return redirect('doctor_register')
        else:
            staff = Doctor.objects.create_user(username,firstname,lastname,email,mobile,
            address,staff_type,password)
            #creating a STAFF group
            staff.save()
            doctor_group = Group.objects.get_or_create(name='STAFF')
            doctor_group[0].user_set.add(staff)
            login(request,staff)
            messages.success(request,"Account Created!")
            print('account created')
            return redirect('home')
    else:
        return render(request,'hospital/home.html')



@csrf_protect
def patient_register(request):
    if request.method == 'POST':

        doctor = request.POST.get('doctor')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        symptoms = request.POST.get('symptoms')
        disease = request.POST.get('disease')
        file = request.FILES['file_upload']
        
        if Patient.objects.filter(mobile=mobile).exists():
            messages.info(request,'Patient with this mobile number already exists')
            return render(request,'hospital/doctor_page.html')
        else:
            patient = Patient(doctor,fname,lname,mobile,address,symptoms,disease,file)
            messages.info(request,'Patient Registered Successfully!!')
            patient.save()

        return render(request,'hospital/doctor_page.html')


def user_register(request):
    if request.method == 'POST':
        email = request.POST['email']
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        department = request.POST.get('department')
        password = request.POST.get('pwd')

        if User.objects.filter(mobile=mobile).exists():
            messages.info(request,'mobile exists!')
            print('mobile exists')
            return redirect('doctor_register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email exists!')
            return redirect('doctor_register')
        else:
            
            user = User.objects.create_user(email,mobile,
            address,department,password)
            user.save()
            login(request,user)
            messages.success(request,"Account Created!")
            print('account created')
            return redirect('home')
    else:
        return render(request,'hospital/home.html')

def appointment_booking(request):
    if request.method == 'GET':
        fname = request.GET.get('fname')
        lname = request.GET.get('lname')
        mobile = request.GET.get('mobile')
        symptoms = request.GET.get('symptoms')
        date = request.GET.get('date')
        time = request.GET.get('time')

        appoint = Appointment(fname=fname,lname=lname,mobile=mobile,symptoms=symptoms,date=date,time=time)
        appoint.save()
    return redirect('home')

def logout(request):
    auth.logout(request)
    return render(request,'hospital/home.html')