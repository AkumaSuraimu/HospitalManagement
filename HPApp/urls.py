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
    
    path('patient/', views.patient_LP, name='patient_LP'),
    path('patient/booking', views.patient_book_appointment, name='patient_book_appointment'),
    path('patient/medicalrecord', views.patient_med_record, name='patient_med_record'),
    path('patient/billing', views.patient_view_billing, name='patient_view_billing'),
    
    # added staff and other link, nothing for dashboards yet
    path('staff/', views.staff_LP, name='staff_LP'),
    path('staff/addroom', views.staff_add_room, name='staff_add_room'),
    path('staff/addbilling', views.staff_add_billing, name='staff_add_billing'),
    path('staff/viewrooms', views.staff_view_rooms, name='staff_view_rooms'),
    path('staff/viewBR', views.staff_view_BR, name='staff_view_BR'),
]