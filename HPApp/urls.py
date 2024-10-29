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


    path('doctor/', views.doctor_LP, name='doctor_LP'),
    path('patient/', views.patient_LP, name='patient_LP'),
    path('staff/', views.staff_LP, name='staff_LP'),
]