from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password,make_password
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from . import models

# Create your views here.
def user_list(request):
    
    users = models.User.objects.all()
    
    doctors = models.Doctor.objects.select_related('user', 'staff').all()
    patients = models.Patient.objects.select_related('user').all()
    staff = models.Staff.objects.select_related('user').all()

    return render(request, 'user_list.html', {
        'users': users,
        'doctors': doctors,
        'patients': patients,
        'staff': staff,
    })

def patient_register(request):
    return render(request, 'patient_register.html')

def doctor_register(request):
    return render(request, 'doctor_register.html')

def staff_register(request):
    return render(request, 'staff_register.html')

def custom_logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your preferred page

@login_required
def doctor_LP(request):
    try:
        # Get the doctor profile associated with the user
        doctor = models.Doctor.objects.get(user=request.user)
        
        # Fetch schedule and list of all patients
        schedule = models.Schedule.objects.filter(doctor=doctor)
        patients = models.Patient.objects.all()
        
        context = {
            'doctor': doctor,
            'schedule': schedule,
            'patients': patients,
        }
        return render(request, 'doctor_LP.html', context)

    except models.Doctor.DoesNotExist:
        # Return an error message if no doctor profile is found
        return render(request, 'doctor_LP.html', {'error': 'No doctor profile associated with this user.'})

@login_required
def staff_LP(request):
    try:
        # Get the staff profile associated with the user
        staff = models.Staff.objects.get(user=request.user)
        
        # Fetch billing records related to the staff
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
        # Get the patient profile associated with the user
        patient = models.Patient.objects.get(user=request.user)
        
        # Fetch billing and schedule records related to the patient
        billing = models.Billing.objects.filter(patient=patient)
        schedule = models.Schedule.objects.filter(patient=patient)
        
        context = {
            'patient': patient,
            'billing': billing,
            'schedule': schedule,
        }
        return render(request, 'patient_LP.html', context)

    except models.Patient.DoesNotExist:
        # Return an error message if no patient profile is found
        return render(request, 'patient_LP.html', {'error': 'No patient profile associated with this user.'})


def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if email and password and role:
            # Create the user with the CustomUserManager
            user = models.User.objects.create_user(email=email, password=password, role=role)

            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user is not None:
                # Log in the user
                login(request, user)

                # Redirect based on the user's role
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
            # Create a new Staff instance and associate it with the current user
            staff = models.Staff.objects.create(
                staff_type=staff_type,
                F_name=F_name,
                L_name=L_name,
                user=request.user  # Use the currently logged-in user
            )
            return redirect('staff_LP')  # Redirect to login after successful registration

    return render(request, 'staff_register.html')
@login_required
def register_doctor(request):

    if request.method == 'POST':
        specialization = request.POST.get('specialization')
        F_name = request.POST.get('F_name')
        L_name = request.POST.get('L_name')
        department_id = request.POST.get('department')  # Get the department from the form

        if specialization and department_id:
            # Fetch the department instance safely
            department_instance = get_object_or_404(models.Department, id=department_id)

            # Create a new Doctor instance
            doctor = models.Doctor.objects.create(
                F_name=F_name,
                L_name=L_name,
                specialization=specialization,
                department=department_instance,  # Use the department instance
                user=request.user
            )
            return redirect('doctor_LP')  # Redirect after successful registration

    # Fetch all departments to display in the form
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
            # Create a new Patient instance
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
            return redirect('patient_LP')  # Redirect after successful registration

    return render(request, 'patient_register.html')
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use authenticate to check email and password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            role = user.role  # Get the user's role from your custom User model

            # Redirect based on the user's role
            if role == 'patient':
                return redirect('patient_LP')
            elif role == 'doctor':
                return redirect('doctor_LP')
            elif role == 'staff':
                return redirect('staff_LP')
            else:
                error = "Invalid role."
        else:
            error = "Invalid email or password."

        return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')