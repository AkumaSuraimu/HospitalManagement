from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=30,unique=True)
    role = models.CharField(max_length=20,default='user')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

class Patient(models.Model):
    F_name = models.CharField(max_length=100)
    L_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    bday = models.DateField()
    gender = models.CharField(max_length=10, default='Unknown')
    address = models.CharField(max_length=100, default='N/A')
    phone = models.CharField(max_length=20, default='0000000000')
    bloodgroup = models.CharField(max_length=10, default='Unknown')
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True) 
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Staff(models.Model):
    staff_type = models.CharField(max_length=100, default='General')
    F_name = models.CharField(max_length=100, default='Unknown')
    L_name = models.CharField(max_length=100, default='Unknown')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Department(models.Model):
    dep_name = models.CharField(max_length=100, default='Unknown')

class Doctor(models.Model):
    F_name = models.CharField(max_length=100, default='Unknown')
    L_name = models.CharField(max_length=100, default='Unknown')
    specialization = models.CharField(max_length=100, default='General')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

class Room(models.Model):
    room_type = models.CharField(max_length=100, default='Standard')
    room_price = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None) 

class Schedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, default=None) 
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default=None) 

class Billing(models.Model):
    bill_date = models.DateField()
    bill_amount = models.IntegerField(default=0)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, default=None) 
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, default=None) 
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None) 

class Equipment(models.Model):
    eq_name = models.CharField(max_length=100, default='Unknown')
    eq_type = models.CharField(max_length=100, default='General')
    eq_qty = models.IntegerField(default=0)
    eq_price = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None)