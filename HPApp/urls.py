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

    path('patient/', views.patient_LP, name='patient_LP'),
    path('patient/edit', views.edit_patient, name='patient_edit'),

    path('staff/', views.staff_LP, name='staff_LP'),
    path('staff/edit', views.edit_staff, name='staff_edit'),

    path('adminLP/', views.admin_LP, name='admin_LP'),
    path('add_admin/', views.add_admin_page, name='admin_addAdmin'),
    path('add-equipment/', views.add_equipment_page, name='admin_addEquipment'),
    path('add-department/', views.add_department_page, name='admin_addDepartment'),
    path('get_user_details/<int:user_id>/', views.get_user_details, name='get_user_details'),
    

]