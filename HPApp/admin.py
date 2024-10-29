from django.contrib import admin
from . import models

# Register your models here

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')  # Removed password for security
    search_fields = ('email',)  # Allows searching by email

@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'L_name', 'F_name','specialization','department', 'user')
    search_fields = ('specialization',)  # Allows searching by specialization

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'F_name', 'L_name', 'user')
    search_fields = ('F_name', 'L_name')  # Allows searching by first or last name

@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id','staff_type','F_name', 'L_name', 'user')
    search_fields = ('F_name', 'L_name')  # Allows searching by first or last name

@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'dep_name')
    search_fields = ('dep_name', 'specialization')  # Allows searching by department name

@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_type', 'room_price', 'department')
    search_fields = ('room_type',)  # Allows searching by room type

@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'doctor', 'patient')
    search_fields = ('date',)  # Allows searching by date

@admin.register(models.Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('id', 'bill_date', 'bill_amount', 'patient', 'staff', 'department')
    search_fields = ('bill_date', 'patient__F_name', 'patient__L_name')  # Allows searching by bill date or patient name

@admin.register(models.Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'eq_name', 'eq_type', 'eq_qty', 'eq_price', 'department')
    search_fields = ('eq_name',)  # Allows searching by equipment name
