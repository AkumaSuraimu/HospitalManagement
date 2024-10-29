# forms.py
from django import forms
from .models import User, Patient, Staff, Department, Doctor, Room, Schedule, Billing, Equipment

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'role']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['F_name', 'L_name', 'age', 'bday', 'gender', 'address', 'phone', 'email', 'bloodgroup', 'room', 'user']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['staff_type', 'F_name', 'L_name', 'user']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dep_name', 'specialization', 'staff']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctor_type', 'specialization', 'staff', 'user']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_type', 'room_price', 'department']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['date', 'time', 'doctor', 'patient']

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['bill_date', 'bill_amount', 'patient', 'staff', 'department']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['eq_name', 'eq_type', 'eq_qty', 'eq_price', 'department']
