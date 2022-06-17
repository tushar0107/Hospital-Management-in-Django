from asyncore import dispatcher_with_send
from email.policy import default
from inspect import modulesbyfile
from operator import truediv
from pickle import TRUE
from pyexpat import model
from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model



# Create your models here.

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Orthopedics','Orthopedics'),
('Physiotherapist','Physiotherapist'),
('Gynecologist','Gynecologist'),
('Neurologist','Neurologist'),
('Pediatrist','Pediatrist'),
('Urologist','Urologist')
]

staff_types = [
            ('Doctor','Doctor'),
            ('Nurse','Nurse'),
            ('Ward Boy','Ward Boy'),
            ('Receptionist','Receptionist'),
]


User = get_user_model()

class User(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10,blank=True, null=True)
    department = models.CharField(max_length=40,choices=departments, blank=True,null=True)
    password = models.CharField(max_length=256,null=True)

    def __str__(self):
        return str(self.id)

class Doctor(models.Model):
    username = models.CharField(max_length=20, null=True , unique= True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    address = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10,blank=True, null=True)
    department = models.CharField(max_length=40,choices=departments, blank=False,null=False)
    password = models.CharField(max_length=16,null=True)

    def __str__(self):
        return self.firstname



def user_directory_path(instance,filename=None):
    return '{0}_{1}_{2}'.format(instance.fname,instance.lname,filename)

class Appointment(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True),
    doctor = models.OneToOneField(Doctor,on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=10, null=True)
    symptoms = models.CharField(max_length=200,null=True)
    date = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return self.fname + ' ' + self.lname

class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=200,null=True)
    symptoms = models.CharField(max_length=200,null=True)
    disease = models.CharField(max_length=200,null=True)
    admitdate = models.DateTimeField(blank=True,null=True,default=timezone.now)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return str(self.fname)
        #return self.fname + ' ' + self.lname
  
class Staff(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True,unique=True)
    username = models.CharField(max_length=20, null=True , unique= True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    mobile = models.CharField(max_length=10,blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    staff_type = models.CharField(max_length=20,choices=staff_types, null=True)
    password = models.CharField(max_length=16,null=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname