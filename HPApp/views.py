from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password,make_password
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse,Http404
from . import models
from django.http import JsonResponse
from django.core.paginator import Paginator

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
        
        
        billing = models.Billing.objects.filter(patient=patient)
        schedule = models.Schedule.objects.filter(patient=patient)
        
        context = {
            'patient': patient,
            'billing': billing,
            'schedule': schedule,
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
            staff.save()
            return redirect('staff_LP')  

        return render(request, 'edit_staff.html', {'staff': staff})
    except Http404:
        return redirect('staff_register')