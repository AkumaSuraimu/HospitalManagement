import json
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password,make_password
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse,Http404
from . import models
from django.utils.timezone import now
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta

# Create your views here.
@login_required
def get_user_details(request, user_id):
    try:
        user = get_object_or_404(models.User, id=user_id)
        role_data = {}
        
        if user.role == "patient":
            try:
                patient = models.Patient.objects.get(user=user)
                role_data = {
                    "First Name": patient.F_name,
                    "Last Name": patient.L_name,
                    "Age": patient.age,
                    "Birthday": patient.bday,
                    "Gender": patient.gender,
                    "Address": patient.address,
                    "Phone": patient.phone,
                    "Bloodgroup": patient.bloodgroup,
                    "Room": patient.room.room_type if patient.room else "None",
                }
            except models.Patient.DoesNotExist:
                return JsonResponse({"success": False, "error": "Patient data not found for this user"})
        elif user.role == "staff":
            try:
                staff = models.Staff.objects.get(user=user)
                role_data = {
                    "First Name": staff.F_name,
                    "Last Name": staff.L_name,
                    "Staff Type": staff.staff_type,
                }
            except models.Staff.DoesNotExist:
                return JsonResponse({"success": False, "error": "Staff data not found for this user"})
        elif user.role == "doctor":
            try:
                doctor = models.Doctor.objects.get(user=user)
                role_data = {
                    "First Name": doctor.F_name,
                    "Last Name": doctor.L_name,
                    "Specialization": doctor.specialization,
                    "Department": doctor.department.dep_name if doctor.department else "None",
                }
            except models.Doctor.DoesNotExist:
                return JsonResponse({"success": False, "error": "Doctor data not found for this user"})

        
        print(f"Role Data for user {user_id}: {role_data}")
        
        return JsonResponse({"success": True, "role_data": role_data, "role": user.role})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
    
@login_required
def add_admin_page(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email already exists
        if models.User.objects.filter(email=email).exists():
            context['error'] = "Email already exists."
        else:
            models.User.objects.create(email=email, password=password, role='user', is_staff=True, is_superuser=True)
            context['success'] = "Admin added successfully."

    return render(request, 'admin_addAdmin.html', context)

@login_required
def add_equipment_page(request):
    context = {}

    if request.method == 'POST':
        eq_name = request.POST.get('eq_name')
        eq_type = request.POST.get('eq_type')
        eq_qty = request.POST.get('eq_qty')
        eq_price = request.POST.get('eq_price')
        department_id = request.POST.get('department')

        # Validate the form data
        if not eq_name or not eq_qty or not eq_price:
            context['error'] = "All fields are required."
        else:
            try:
                department = models.Department.objects.get(id=department_id)
                models.Equipment.objects.create(
                    eq_name=eq_name,
                    eq_type=eq_type,
                    eq_qty=int(eq_qty),
                    eq_price=int(eq_price),
                    department=department,
                )
                context['success'] = "Equipment added successfully."
            except models.Department.DoesNotExist:
                context['error'] = "Selected department does not exist."

    # Pass all departments to the template for the department dropdown
    context['departments'] = models.Department.objects.all()
    return render(request, 'admin_addEquipment.html', context)

@login_required
def add_department_page(request):
    context = {}

    if request.method == 'POST':
        dep_name = request.POST.get('dep_name')

        if not dep_name:
            context['error'] = "Department name is required."
        else:
            try:
                models.Department.objects.create(dep_name=dep_name)
                context['success'] = "Department added successfully."
            except Exception as e:
                context['error'] = f"An error occurred: {str(e)}"
    
    return render(request, 'admin_addDepartment.html', context)

def patient_register(request):
    return render(request, 'patient_register.html')

def doctor_register(request):
    return render(request, 'doctor_register.html')

def staff_register(request):
    return render(request, 'staff_register.html')

def custom_logout_view(request):
    logout(request)
    return redirect('login') 

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    
    return redirect('login')

@login_required
def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(models.Equipment, id=equipment_id)
    if equipment.delete():
        return JsonResponse({'success': True,'message': 'Equipment deleted successfully'})
    else:
        return JsonResponse({'success': False,'message': 'Error deleting equipment'}, status=500)

@login_required
def delete_department(request, department_id):
    department = get_object_or_404(models.Department, id=department_id)
    if department.delete():
        return JsonResponse({'success': True,'message': 'Department deleted successfully'})
    else:
        return JsonResponse({'success': False,'message': 'Error deleting department'}, status=500)

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(models.User, id=user_id)
    if user.delete():
        return JsonResponse({'success': True, 'message': 'User deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Error deleting user'}, status=500)

@login_required
def doctor_LP(request):
    try:
        
        doctor = models.Doctor.objects.get(user=request.user)
        
        
        schedule = models.Schedule.objects.filter(doctor=doctor)
        patients = models.Patient.objects.all()
        
        context = {
            'doctor': doctor,
            'schedule': schedule,
            'patients': patients,
        }
        return render(request, 'doctor_LP.html', context)

    except models.Doctor.DoesNotExist:
        
        return render(request, 'doctor_LP.html', {'error': 'No doctor profile associated with this user.'})

@login_required
def staff_LP(request):
    try:
        
        staff = models.Staff.objects.get(user=request.user)
        
       
        billing_records = models.Billing.objects.filter(staff=staff)

        context = {
            'staff': staff,
            'billing_records': billing_records,
        }
        return render(request, 'staff_LP.html', context)

    except models.Staff.DoesNotExist:
        return render(request, 'staff_LP.html', {'error': 'No staff profile associated with this user.'})

@login_required
def patient_LP(request):
    try:
        
        patient = models.Patient.objects.get(user=request.user)
        
        
        billing_records = models.Billing.objects.filter(patient=patient)
        schedule = models.Schedule.objects.filter(patient=patient)
        medical_records = models.MedicalRecord.objects.filter(patient=patient)
        
        context = {
            'patient': patient,
            'billing_records': billing_records,
            'schedule': schedule,
            'medical_records': medical_records,
        }
        return render(request, 'patient_LP.html', context)

    except models.Patient.DoesNotExist:
        
        return render(request, 'patient_LP.html', {'error': 'No patient profile associated with this user.'})


@login_required
def admin_LP(request):
    
    users = models.User.objects.all()

    
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    
    return render(request, 'admin_LP.html', {
        'page_obj': page_obj,  
        'logged_in_user': request.user,
    })



@login_required
def admin_LP(request):
    users = models.User.objects.all()
    equipment_list = models.Equipment.objects.all()
    department_list = models.Department.objects.all()
    staff_time_records = models.TimeInAndOutStaff.objects.select_related('staff').order_by('-time_in')
    doctor_time_records = models.TimeInAndOutDoctor.objects.select_related('doctor').order_by('-time_in')

    # Paginate users
    user_paginator = Paginator(users, 5)
    user_page_number = request.GET.get('page')
    page_obj = user_paginator.get_page(user_page_number)

    # Paginate equipment
    equipment_paginator = Paginator(equipment_list, 5)
    equipment_page_number = request.GET.get('equipment_page')
    equipment_page_obj = equipment_paginator.get_page(equipment_page_number)

    # Paginate departments
    department_paginator = Paginator(department_list, 5)
    department_page_number = request.GET.get('department_page')
    department_page_obj = department_paginator.get_page(department_page_number)

    # Paginate time records for staff
    staff_paginator = Paginator(staff_time_records, 5)
    staff_page_number = request.GET.get('staff_page')
    staff_page_obj = staff_paginator.get_page(staff_page_number)

    # Paginate time records for doctors
    doctor_paginator = Paginator(doctor_time_records, 5)
    doctor_page_number = request.GET.get('doctor_page')
    doctor_page_obj = doctor_paginator.get_page(doctor_page_number)

    return render(request, 'admin_LP.html', {
        'page_obj': page_obj,
        'equipment_page_obj': equipment_page_obj,
        'department_page_obj': department_page_obj,
        'staff_page_obj': staff_page_obj,
        'doctor_page_obj': doctor_page_obj,
        'logged_in_user': request.user,
    })



def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if email and password and role:
            
            if models.User.objects.filter(email=email).exists():
                error = "An account with this email already exists."
                return render(request, "register_user.html", {"error": error})
            
            
            user = models.User.objects.create_user(email=email, password=password, role=role)

            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                
                login(request, user)

                
                if role == 'patient':
                    return redirect('patient_register')
                elif role == 'doctor':
                    return redirect('doctor_register')
                elif role == 'staff':
                    return redirect('staff_register')
                else:
                    return redirect('user_list')

    return render(request, 'register_user.html')

@login_required
def register_staff(request):
    if request.method == 'POST':
        staff_type = request.POST.get('staff_type')
        F_name = request.POST.get('F_name')
        L_name = request.POST.get('L_name')

        if staff_type and F_name and L_name:
            
            staff = models.Staff.objects.create(
                staff_type=staff_type,
                F_name=F_name,
                L_name=L_name,
                user=request.user  
            )
            return redirect('staff_LP')  

    return render(request, 'staff_register.html')

@login_required
def register_doctor(request):

    if request.method == 'POST':
        specialization = request.POST.get('specialization')
        F_name = request.POST.get('F_name')
        L_name = request.POST.get('L_name')
        department_id = request.POST.get('department')  

        if specialization and department_id:
            
            department_instance = get_object_or_404(models.Department, id=department_id)

            
            doctor = models.Doctor.objects.create(
                F_name=F_name,
                L_name=L_name,
                specialization=specialization,
                department=department_instance,  
                user=request.user
            )
            return redirect('doctor_LP') 

    departments = models.Department.objects.all()

    return render(request, 'doctor_register.html', {'departments': departments})

@login_required
def register_patient(request):

    if request.method == 'POST':
        F_name = request.POST.get('F_name')
        L_name = request.POST.get('L_name')
        age = request.POST.get('age')
        bday = request.POST.get('bday')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        bloodgroup = request.POST.get('bloodgroup')

        if F_name and L_name and age and bday and gender:
            patient = models.Patient.objects.create(
                F_name=F_name,
                L_name=L_name,
                age=age,
                bday=bday,
                gender=gender,
                address=address,
                phone=phone,
                bloodgroup=bloodgroup,
                user=request.user
            )
            return redirect('patient_LP')  

    return render(request, 'patient_register.html')

def login_view(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                role = user.role  

                if role == 'patient':
                    return redirect('patient_LP')
                elif role == 'doctor':
                    return redirect('doctor_LP')
                elif role == 'staff':
                    return redirect('staff_LP')
                elif role == 'user':
                    return redirect('admin_LP')
                else:
                    error = "Invalid role."
            else:
                error = "Invalid email or password."

            return render(request, 'login.html', {'error': error})

        return render(request, 'login.html')
    else:
        role = request.user.role  

        if role == 'patient':
            return redirect('patient_LP')
        elif role == 'doctor':
            return redirect('doctor_LP')
        elif role == 'staff':
            return redirect('staff_LP')
        elif role == 'user':
            return redirect('admin_LP')

@login_required
def edit_patient(request):
    try:
        user = models.Patient.objects.get(user=request.user)
        if request.method == 'POST':
            F_name = request.POST.get('F_name')
            L_name = request.POST.get('L_name')
            age = request.POST.get('age')
            bday = request.POST.get('bday')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            bloodgroup = request.POST.get('bloodgroup')

            user.F_name = F_name
            user.L_name = L_name
            user.age = age
            user.bday = bday
            user.gender = gender
            user.address = address
            user.phone = phone
            user.bloodgroup = bloodgroup

            # Handle image upload
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']
            user.save()
            return redirect('patient_LP')

        return render(request,'edit_patient.html',{'user':user})
    except Http404:
        return redirect('patient_register')

@login_required
def edit_doctor(request):
    try:
        doctor = get_object_or_404(models.Doctor, user=request.user) 
        departments = models.Department.objects.all() 
        for department in departments:
            print(department.dep_name)
        if request.method == 'POST':
            doctor.F_name = request.POST.get('F_name')
            doctor.L_name = request.POST.get('L_name')
            doctor.specialization = request.POST.get('specialization')
            doctor.department_id = request.POST.get('department')  
            # Handle image upload
            if 'profile_image' in request.FILES:
                doctor.profile_image = request.FILES['profile_image']
            doctor.save()
            return redirect('doctor_LP')  

        return render(request, 'edit_doctor.html', {'doctor': doctor, 'departments': departments})
    except Http404:
        return redirect('doctor_register')

@login_required
def edit_staff(request):
    try:
        staff = get_object_or_404(models.Staff, user=request.user) 

        if request.method == 'POST':
            staff.F_name = request.POST.get('F_name')
            staff.L_name = request.POST.get('L_name')
            staff.staff_type = request.POST.get('staff_type')
            # Handle image upload
            if 'profile_image' in request.FILES:
                staff.profile_image = request.FILES['profile_image']
            staff.save()
            return redirect('staff_LP')  

        return render(request, 'edit_staff.html', {'staff': staff})
    except Http404:
        return redirect('staff_register')
    
@login_required
def admin_billing_management(request):
    success_message = ""
    selected_billing = None
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    billing_records = models.Billing.objects.all()
    
    if request.method == 'GET' and 'edit_billing' in request.GET:
        bill_id = request.GET.get('edit_billing')
        try:
            selected_billing = models.Billing.objects.get(id=bill_id)
        except models.Billing.DoesNotExist:
            success_message = "Selected billing record does not exist."
    
    if request.method == 'POST' and 'add_billing' in request.POST:
        bill_date = request.POST.get('bill_date')
        bill_amount = request.POST.get('bill_amount')
        patient_id = request.POST.get('patient_id')
        department_id = request.POST.get('department_id')
        
        if bill_date and bill_amount and patient_id and department_id:
            patient = models.Patient.objects.get(id = patient_id)
            department = models.Department.objects.get(id = department_id)
            
            billing = models.Billing.objects.create(
                bill_date = bill_date,
                bill_amount = bill_amount,
                patient = patient,
                department = department
            )
            success_message = "Billing record added successfully!"
            
    if request.method == 'POST' and 'update_billing' in request.POST:
        bill_id = request.POST.get('bill_id')
        bill_date = request.POST.get('bill_date')
        bill_amount = request.POST.get('bill_amount')
        patient_id = request.POST.get('patient_id')
        department_id = request.POST.get('department_id')
        
        if bill_id and bill_date and bill_amount and patient_id and department_id:
            billing = models.Billing.objects.get(id = bill_id)
            
            billing.bill_date = bill_date
            billing.bill_amount = bill_amount
            billing.patient = models.Patient.objects.get(id = patient_id)
            billing.department = models.Department.objects.get(id = department_id)
            billing.save()
            
            success_message = "Billing record updated successfully!"
        
    if request.method == 'POST' and 'delete_billing' in request.POST:
        bill_id = request.POST.get('bill_id')
        
        if bill_id:
            try:
                billing = models.Billing.objects.get(id = bill_id)
                billing.delete()
                success_message = "Billing record deleted successfully!"
            except models.Billing.DoesNotExist:
                success_message = "Billing record does not exist"
        
    patients = models.Patient.objects.all()
    departments = models.Department.objects.all()
        
    return render(request, 'admin_billing_management.html', {
        'billing_records': billing_records,
        'patients': patients,
        'departments': departments,
        'success_message': success_message,
        'selected_billing': selected_billing,
        'today_date': today_date
        }
    )

@login_required
def admin_room_management(request):
    success_message = ""
    selected_room = None
    
    rooms = models.Room.objects.all()
    departments = models.Department.objects.all()
    
    if request.method == 'GET' and 'edit_room' in request.GET:
        room_id = request.GET.get('edit_room')
        try:
            selected_room = models.Room.objects.get(id=room_id)
        except models.Room.DoesNotExist:
            success_message = "Selected room does not exist."
    
    if request.method == 'POST' and 'add_room' in request.POST:
        room_type = request.POST.get('room_type')
        room_price = request.POST.get('room_price')
        department_id = request.POST.get('department_id')
        
        if room_type and room_price and department_id:
            department = models.Department.objects.get(id = department_id)
            models.Room.objects.create(
                room_type = room_type,
                room_price = room_price,
                department = department
            )
            success_message = "Room added successfully!"
            
    if request.method == 'POST' and 'update_room' in request.POST:
        room_id = request.POST.get('room_id')
        room_type = request.POST.get('room_type')
        room_price = request.POST.get('room_price')
        department_id = request.POST.get('department_id')
        
        if room_id and room_type and room_price and department_id:
            department = models.Department.objects.get(id = department_id)
            room = models.Room.objects.get(id = room_id)
            
            room.room_type = room_type
            room.room_price = room_price
            room.department = department
            room.save()
            
            success_message = "Room updated successfully!"
            
    if request.method == 'POST' and 'delete_room' in request.POST:
        room_id = request.POST.get('room_id')
        
        if room_id:
            try:
                room = models.Room.objects.get(id = room_id)
                room.delete()
                success_message = "Room deleted successfully!"
            except models.Room.DoesNotExist:
                success_message - "Room not found!"
    
    return render(request, 'admin_room_management.html', {
        'rooms': rooms,
        'departments': departments,
        'success_message': success_message,
        'selected_room': selected_room
    })
    
@login_required
def admin_equipment_management(request):
    success_message = ""
    selected_equipment = None
    
    equipment = models.Equipment.objects.all()
    departments = models.Department.objects.all()
    
    if request.method == 'GET' and 'edit_equipment' in request.GET:
        equipment_id = request.GET.get('edit_equipment')
        
        if equipment_id:
            try:
                selected_equipment = models.Equipment.objects.get(id = equipment_id)
            except models.Equipment.DoesNotExist:
                success_message = "Equipment not found."
                
    if request.method == 'POST' and 'add_equipment' in request.POST:
        eq_name = request.POST.get('eq_name')
        eq_type = request.POST.get('eq_type')
        eq_qty = request.POST.get('eq_qty')
        eq_price = request.POST.get('eq_price')
        department_id = request.POST.get('department_id')
        
        if eq_name and eq_type and eq_qty and eq_price and department_id:
            department = models.Department.objects.get(id = department_id)
            
            models.Equipment.objects.create(
                eq_name = eq_name,
                eq_type = eq_type,
                eq_qty = eq_qty,
                eq_price = eq_price,
                department = department
            )
            success_message = "Equipment created successfully!"
    
    if request.method == 'POST' and 'update_equipment' in request.POST:
        equipment_id = request.POST.get('equipment_id')
        eq_name = request.POST.get('eq_name')
        eq_type = request.POST.get('eq_type')
        eq_qty = request.POST.get('eq_qty')
        eq_price = request.POST.get('eq_price')
        department_id = request.POST.get('department_id')
        
        if equipment_id and eq_name and eq_type and eq_qty and eq_price and department_id:
            try:
                equipment_instance = models.Equipment.objects.get(id = equipment_id)
                department = models.Department.objects.get(id = department_id)
                
                equipment_instance.eq_name = eq_name
                equipment_instance.eq_type = eq_type
                equipment_instance.eq_qty = eq_qty
                equipment_instance.eq_price = eq_price
                equipment_instance.department = department
                
                equipment_instance.save()
                
                success_message = "Equipment updated successfully!"
            except models.Equipment.DoesNotExist:
                success_message = "Equipment not found/does not exist."
            except models.Department.DoesNotExist:
                success_message = "Department does not exist?"
                
    if request.method == 'POST' and 'delete_equipment' in request.POST:
        equipment_id = request.POST.get('equipment_id')
        
        if equipment_id:
            try:
                equipment_instance = models.Equipment.objects.get(id = equipment_id)
                equipment_instance.delete()
                success_message = "Equipment deleted successfully!"
            except models.Equipment.DoesNotExist:
                success_message = "Equipment not found!"
                
    return render(request, 'admin_equipment_management.html', {
        'equipment': equipment,
        'success_message': success_message,
        'selected_equipment': selected_equipment,
        'departments': departments,
    })

@login_required
def patient_book_appointment(request):
    try:
        patient = models.Patient.objects.get(user = request.user)
    except models.Patient.DoesNotExist:
        return redirect('patient_LP')
    
    appointments = models.Schedule.objects.filter(patient=patient).order_by('date', 'time')
    
    success_message = ""
    
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        doctor_id = request.POST.get('doctor')
        
        if date and time and doctor_id:
            doctor = models.Doctor.objects.get(id = doctor_id)
            
            models.Schedule.objects.create(
                date = date,
                time = time,
                doctor = doctor,
                patient = patient
            )
            success_message = "Appointment booked successfully!"
        
    doctors = models.Doctor.objects.all()
    
    return render(request, 'patient_book_appointment.html', {
        'patient': patient,
        'appointments': appointments,
        'doctors': doctors,
        'success_message': success_message,
    })
    
@login_required
def patient_med_record(request):
    try:
        patient = models.Patient.objects.get(user = request.user)
    except models.Patient.DoesNotExist:
        return redirect('patient_LP')
    
    medical_records = models.MedicalRecord.objects.filter(patient = patient).order_by('-date')
    
    return render(request, 'patient_med_record.html', {
        'patient': patient,
        'medical_records': medical_records,
    })

@login_required
def patient_view_billing(request):
    try:
        patient = models.Patient.objects.get(user = request.user)
    except models.Patient.DoesNotExist:
        return redirect('patient_LP')
    
    billing_records = models.Billing.objects.filter(patient = patient).order_by('bill_date')
    
    return render(request, 'patient_view_billing.html', {
        'patient': patient,
        'billing_records': billing_records,
    })
    
@login_required
def doctor_check_appointments(request):
    try:
        doctor = models.Doctor.objects.get(user = request.user)
    except models.Doctor.DoesNotExist:
        return redirect('doctor_LP')
    
    patients = models.Patient.objects.filter(schedule__doctor = doctor).distinct()
    appointments = models.Schedule.objects.filter(doctor = doctor).order_by('date', 'time')
    
    success_message = ""
    selected_appointment = None
    now = datetime.now()
    today_date = now.strftime('%Y-%m-%d')
    min_time = now.strftime('%H:%M') if now.hour >= 10 else "10:00"
    
    if request.method == 'GET' and 'edit_appointment' in request.GET:
        appointment_id = request.GET.get('edit_appointment')
        try:
            selected_appointment = models.Schedule.objects.get(id = appointment_id)
        except models.Schedule.DoesNotExist:
            success_message = "Selected appointment does not exist."
    
    if request.method == 'POST' and 'add_appointment' in request.POST:
        date = request.POST.get('date')
        time = request.POST.get('time')
        patient_id = request.POST.get('patient_id')
        
        if date and time and patient_id:
            patient = models.Patient.objects.get(id = patient_id)
            
            models.Schedule.objects.create(
                date = date,
                time = time,
                doctor = doctor,
                patient = patient
            )
            
            success_message = "Appointment added successfully!"
    
    if request.method == 'POST' and 'update_appointment' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        patient_id = request.POST.get('patient_id')
        
        if appointment_id and date and time and patient_id:
            appointment = models.Schedule.objects.get(id = appointment_id)
            patient = models.Patient.objects.get(id = patient_id)
            
            appointment.date = date
            appointment.time = time
            appointment.patient = patient
            appointment.doctor = doctor
            appointment.save()
            
            success_message = "Appointment updated successfully!"
    
    if request.method == 'POST' and 'delete_appointment' in request.POST:
        appointment_id = request.POST.get('appointment_id')
        
        if appointment_id:
            try:
                appointment = models.Schedule.objects.get(id = appointment_id)
                appointment.delete()
                success_message = "Appointment deleted successfully!"
            except models.Schedule.DoesNotExist:
                success_message = "Appointment not found!"
    
    return render(request, 'doctor_check_appointments.html', {
        'doctor': doctor,
        'patients': patients,
        'appointments': appointments,
        'success_message': success_message,
        'selected_appointment': selected_appointment,
        'today_date': today_date,
        'min_time': min_time,
    })
    
@login_required
def doctor_view_patients(request):
    try:
        doctor = models.Doctor.objects.get(user = request.user)
    except models.Doctor.DoesNotExist:
        return redirect('doctor_LP')
    
    patients = models.Patient.objects.all()
    
    return render(request, 'doctor_view_patients.html', {
        'doctor': doctor,
        'patients': patients,
    })
    
@login_required
def doctor_view_billing(request):
    try:
        doctor = models.Doctor.objects.get(user = request.user)
    except models.Doctor.DoesNotExist:
        return redirect('doctor_LP')
    
    
    billings = models.Billing.objects.all()
    
    return render(request, 'doctor_view_billing.html', {
        'doctor': doctor,
        'billings': billings,
    })
    
@login_required
def doctor_med_record_management(request):
    try:
        doctor = models.Doctor.objects.get(user = request.user)
    except models.Doctor.DoesNotExist:
        return redirect('doctor_LP')
    
    success_message = ""
    selected_med_record = None
    
    patients = models.Patient.objects.all()
    med_records = models.MedicalRecord.objects.filter(doctor = doctor).order_by('date')
    
    if request.method == 'GET' and 'edit_med_record' in request.GET:
        med_record_id = request.GET.get('edit_med_record')
        
        try:
            selected_med_record = models.MedicalRecord.objects.get(id = med_record_id)
        except models.MedicalRecord.DoesNotExist:
            success_message = "Medical Record does not exist!"
    
    if request.method == 'POST' and 'add_med_record' in request.POST:
        patient_id = request.POST.get('patient_id')
        date = request.POST.get('date')
        details = request.POST.get('details')
        
        if patient_id and date and details:
            patient = models.Patient.objects.get(id = patient_id)
            
            models.MedicalRecord.objects.create(
                patient = patient,
                doctor = doctor,
                date = date,
                details = details
            )
            success_message = "Medical Record added successfully!"
    
    if request.method == 'POST' and 'update_med_record' in request.POST:
        med_record_id = request.POST.get('med_record_id')
        patient_id = request.POST.get('patient_id')
        date = request.POST.get('date')
        details = request.POST.get('details')
        
        if med_record_id and patient_id and date and details:
            try:
                med_record = models.MedicalRecord.objects.get(id = med_record_id)
                patient = models.Patient.objects.get(id = patient_id)
                
                med_record.patient = patient
                med_record.date = date
                med_record.details = details
                
                med_record.save()
                
                success_message = "Medical Record updated successfully!"
            except models.MedicalRecord.DoesNotExist:
                success_message = "Medical Record does not exist."
            except models.Patient.DoesNotExist:
                success_message = "Patient does not exist."
    
    if request.method == 'POST' and 'delete_med_record' in request.POST:
        med_record_id = request.POST.get('med_record_id')
        
        if med_record_id:
            try:
                med_record = models.MedicalRecord.objects.get(id = med_record_id)
                med_record.delete()
                success_message = "Medical Record deleted successfully!"
            except models.MedicalRecord.DoesNotExist:
                success_message = "Medical Record not found!"
    
    return render(request, 'doctor_med_record_management.html', {
        'doctor': doctor,
        'patients': patients,
        'med_records': med_records,
        'success_message': success_message,
        'selected_med_record': selected_med_record,
    })
    
@login_required
def staff_assign_room(request):
    try:
        staff = models.Staff.objects.get(user = request.user)
    except models.Staff.DoesNotExist:
        return redirect('staff_LP')
    
    success_message = ""
    
    rooms = models.Room.objects.all()
    # patients = models.Patient.objects.all()
    # doctors = models.Doctor.objects.all()
    
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        # patient_id = request.POST.get('patient_id')
        # doctor_id = request.POST.get('doctor_id')
        try:
            room = models.Room.objects.get(id=room_id)
                
            # room.patient = models.Patient.objects.get(id=patient_id)
            # room.doctor = models.Doctor.objects.get(id=doctor_id)
                
            room.save()
                
            success_message = "Room successfully assigned!"
        except models.Room.DoesNotExist:
            success_message = "Room does not exist?"
        # except models.Patient.DoesNotExist:
            # success_message = "Patient does not exist, too?"
        # except models.Doctor.DoesNotExist:
            # success_message = "Doctor also doesn't exist??? What's going on???"
    
    return render(request, 'staff_assign_room.html', {
        'rooms': rooms,
        # 'patients': patients,
        # 'doctors': doctors,
        'staff': staff,
        'success_message': success_message,
    })
    
@require_http_methods(["GET"])
def get_equipment_details(request, equipment_id):
    equipment = get_object_or_404(models.Equipment, id=equipment_id)
    departments = models.Department.objects.all().values('id', 'dep_name')
    data = {
        'id': equipment.id,
        'eq_name': equipment.eq_name,
        'eq_type': equipment.eq_type,
        'eq_qty': equipment.eq_qty,
        'eq_price': equipment.eq_price,
        'department_id': equipment.department.id,
        'department': list(departments)
    }   
    return JsonResponse(data)

@require_http_methods(["GET"])
def get_department_details(request, department_id):
    department = get_object_or_404(models.Department, id=department_id)
    data = {
        'id': department.id,
        'dep_name': department.dep_name
    }
    return JsonResponse(data)

@require_http_methods(["POST"])
def update_equipment(request):
    if request.content_type == 'application/json':
        data = json.loads(request.body)
    else:
        data = request.POST  # For form data submissions

    equipment_id = data.get('id')
    equipment = get_object_or_404(models.Equipment, id=equipment_id)
    
    equipment.eq_name = data.get('eq_name', equipment.eq_name)
    equipment.eq_type = data.get('eq_type', equipment.eq_type)
    equipment.eq_qty = data.get('eq_qty', equipment.eq_qty)
    equipment.eq_price = data.get('eq_price', equipment.eq_price)
    
    department_id = data.get('department')
    print(f"Received department_id: {department_id}")
    if department_id:
        try:
            department = get_object_or_404(models.Department, id=department_id)
            equipment.department = department
        except models.Department.DoesNotExist:
            print(f"Department with ID {department_id} not found.")
    
    equipment.save()
    
    return JsonResponse({'success': True, 'message': 'Equipment updated successfully'})

@require_http_methods(["POST"])
def update_department(request):
    department_id = request.POST.get('id')
    department_name = request.POST.get('dep_name')

    if not department_id or not department_name:
        return JsonResponse({'success': False, 'message': 'Missing required fields: id or dep_name'}, status=400)

    department = get_object_or_404(models.Department, id=department_id)
    department.dep_name = department_name
    department.save()

    return JsonResponse({'success': True, 'message': 'Department updated successfully'})

@login_required
def update_time_in_out(request):
    if request.method == "POST":
        data = json.loads(request.body)
        doctor_id = data.get("doctorId")
        action = data.get("action")

        try:
            # Retrieve the doctor object
            doctor = models.Doctor.objects.get(id=doctor_id)

            if action == "time_in":
                # Create a new time_in record with time_out set to None
                models.TimeInAndOutDoctor.objects.create(doctor=doctor, time_in=now(), time_out=None)
                return JsonResponse({"success": True})

            elif action == "time_out":
                # Find the last record where time_out is None (i.e., current "time_in" record)
                record = models.TimeInAndOutDoctor.objects.filter(doctor=doctor, time_out=None).last()
                
                if record:
                    # Update the last record with the current time as time_out
                    record.time_out = now()
                    record.save()
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({"success": False, "error": "No time-in record found for this doctor."}, status=404)

            else:
                return JsonResponse({"success": False, "error": "Invalid action."}, status=400)

        except models.Doctor.DoesNotExist:
            return JsonResponse({"success": False, "error": "Doctor not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)

@login_required
def update_staff_time_in_out(request):
    if request.method == "POST":
        data = json.loads(request.body)
        staff_id = data.get("staffId")
        action = data.get("action")

        try:
            # Retrieve the staff object
            staff = models.Staff.objects.get(id=staff_id)

            if action == "time_in":
                # Create a new time_in record with time_out set to None
                models.TimeInAndOutStaff.objects.create(staff=staff, time_in=now(), time_out=None)
                return JsonResponse({"success": True, "message": "Time In recorded successfully!"})

            elif action == "time_out":
                # Find the last record where time_out is None (i.e., current "time_in" record)
                record = models.TimeInAndOutStaff.objects.filter(staff=staff, time_out=None).last()
                
                if record:
                    # Update the last record with the current time as time_out
                    record.time_out = now()
                    record.save()
                    return JsonResponse({"success": True, "message": "Time Out recorded successfully!"})
                else:
                    return JsonResponse({"success": False, "error": "No time-in record found for this staff."}, status=404)

            else:
                return JsonResponse({"success": False, "error": "Invalid action."}, status=400)

        except models.Staff.DoesNotExist:
            return JsonResponse({"success": False, "error": "Staff not found."}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)

def delete_doctor_time_record(request, record_id):
    if request.method == 'DELETE':
        record = get_object_or_404(models.TimeInAndOutDoctor, id=record_id)
        record.delete()
        return JsonResponse({'message': 'Doctor time record deleted successfully.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def delete_staff_time_record(request, record_id):
    if request.method == 'DELETE':
        record = get_object_or_404(models.TimeInAndOutStaff, id=record_id)
        record.delete()
        return JsonResponse({'message': 'Staff time record deleted successfully.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)