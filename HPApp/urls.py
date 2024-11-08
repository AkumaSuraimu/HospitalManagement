from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.register_user, name='register_user'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('user-list/', views.user_list, name='user_list'),
    path('register/doctor/', views.register_doctor, name='doctor_register'),
    path('register/patient/', views.register_patient, name='patient_register'),
    path('register/staff', views.register_staff, name='staff_register'),

    path('logout/', views.custom_logout_view, name='logout'),

    # i plan to do the rest for the doctor soon, for now i'm making a pull request to merge these
    path('doctor/', views.doctor_LP, name='doctor_LP'),
    path('doctor/doctor_view_patients', views.doctor_view_patients, name='doctor_view_patients'),
    path('doctor/doctor_view_billing', views.doctor_view_billing, name='doctor_view_billing'),
    path('doctor/doctor_check_appointments', views.doctor_check_appointments, name='doctor_check_appointments'),
    path('doctor/doctor_med_record_management', views.doctor_med_record_management, name='doctor_med_record_management'),
    
    path('patient/', views.patient_LP, name='patient_LP'),
    path('patient/booking', views.patient_book_appointment, name='patient_book_appointment'),
    path('patient/medicalrecord', views.patient_med_record, name='patient_med_record'),
    path('patient/billing', views.patient_view_billing, name='patient_view_billing'),
    
    # added staff and other link, nothing for dashboards yet
    path('staff/', views.staff_LP, name='staff_LP'),
    path('staff/rooms', views.staff_room_management, name='staff_room_management'),
    path('staff/billing', views.staff_billing_management, name='staff_billing_management'),
]