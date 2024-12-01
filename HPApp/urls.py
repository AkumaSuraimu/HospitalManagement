from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.register_user, name='register_user'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('register/doctor/', views.register_doctor, name='doctor_register'),
    path('register/patient/', views.register_patient, name='patient_register'),
    path('register/staff', views.register_staff, name='staff_register'),

     path('logout/', views.custom_logout_view, name='logout'),
     path('delete/', views.delete_user, name='delete'),
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
     path('delete_equipment/<int:equipment_id>/', views.delete_equipment, name='delete_equipment'),
     path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),


    path('doctor/', views.doctor_LP, name='doctor_LP'),
    path('doctor/edit', views.edit_doctor, name='doctor_edit'),
    path('doctor/doctor_view_patients', views.doctor_view_patients, name='doctor_view_patients'),
    path('doctor/doctor_view_billing', views.doctor_view_billing, name='doctor_view_billing'),
    path('doctor/doctor_check_appointments', views.doctor_check_appointments, name='doctor_check_appointments'),
    path('doctor/doctor_med_record_management', views.doctor_med_record_management, name='doctor_med_record_management'),

    path('patient/', views.patient_LP, name='patient_LP'),
    path('patient/edit', views.edit_patient, name='patient_edit'),
    path('patient/booking', views.patient_book_appointment, name='patient_book_appointment'),
    path('patient/medicalrecord', views.patient_med_record, name='patient_med_record'),
    path('patient/billing', views.patient_view_billing, name='patient_view_billing'),

    path('staff/', views.staff_LP, name='staff_LP'),
    path('staff/edit', views.edit_staff, name='staff_edit'),
    path('staff/assign_room', views.staff_assign_room, name='staff_assign_room'),

    path('adminLP/', views.admin_LP, name='admin_LP'),
    path('adminLP/equipment', views.admin_equipment_management, name='admin_equipment_management'),
    path('adminLP/rooms', views.admin_room_management, name='admin_room_management'),
    path('adminLP/billing', views.admin_billing_management, name='admin_billing_management'),
    path('add_admin/', views.add_admin_page, name='admin_addAdmin'),
    path('add-equipment/', views.add_equipment_page, name='admin_addEquipment'),
    path('add-department/', views.add_department_page, name='admin_addDepartment'),
    path('get_user_details/<int:user_id>/', views.get_user_details, name='get_user_details'),

]