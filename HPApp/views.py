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
        return render(request, 'doctor/doctor_LP.html', context)

    except models.Doctor.DoesNotExist:
        # Return an error message if no doctor profile is found
        return render(request, 'doctor/doctor_LP.html', {'error': 'No doctor profile associated with this user.'})

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
        return render(request, 'staff/staff_LP.html', context)

    except models.Staff.DoesNotExist:
        return render(request, 'staff/staff_LP.html', {'error': 'No staff profile associated with this user.'})

@login_required
def patient_LP(request):
    try:
        # Get the patient profile associated with the user
        patient = models.Patient.objects.get(user=request.user)
        
        # Fetch billing and schedule records related to the patient
        billings = models.Billing.objects.filter(patient=patient)
        appointments = models.Schedule.objects.filter(patient=patient)
        
        context = {
            'patient': patient,
            'billings': billings,
            'appointments': appointments,
        }
        return render(request, 'patient/patient_LP.html', context)

    except models.Patient.DoesNotExist:
        # Return an error message if no patient profile is found
        return render(request, 'patient/patient_LP.html', {'error': 'No patient profile associated with this user.'})


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
                    return redirect('patient/patient_register')
                elif role == 'doctor':
                    return redirect('doctor_register')
                elif role == 'staff':
                    return redirect('staff/staff_register')
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

    return render(request, 'staff/staff_register.html')

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

@login_required
def staff_billing_management(request):
    try:
        staff = models.Staff.objects.get(user = request.user)
    except models.Staff.DoesNotExist:
        return redirect('staff_LP')
    
    success_message = ""
    selected_billing = None
    
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
                staff = staff,
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
        
    return render(request, 'staff/staff_billing_management.html', {
        'billing_records': billing_records,
        'patients': patients,
        'departments': departments,
        'success_message': success_message,
        'selected_billing': selected_billing,
        }
    )

@login_required
def staff_room_management(request):
    try:
        staff = models.Staff.objects.get(user = request.user)
    except models.Staff.DoesNotExist:
        return redirect('staff_LP')
    
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
        department_id = request.POST.get('department')
        
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
        department_id = request.POST.get('department')
        
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
    
    return render(request, 'staff/staff_room_management.html', {
        'rooms': rooms,
        'departments': departments,
        'success_message': success_message,
        'selected_room': selected_room
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
    
    return render(request, 'patient/patient_book_appointment.html', {
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
    
    return render(request, 'patient/patient_med_record.html', {
        'patient': patient,
        'medical_records': medical_records,
    })

@login_required
def patient_view_billing(request):
    try:
        patient = models.Patient.objects.get(user = request.user)
    except models.Patient.DoesNotExist:
        return redirect('patient_LP')
    
    billing = models.Billing.objects.filter(patient = patient).order_by('bill_date')
    
    return render(request, 'patient/patient_view_billing.html', {
        'patient': patient,
        'billing': billing,
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
    
    return render(request, 'doctor/doctor_check_appointments.html', {
        'doctor': doctor,
        'patients': patients,
        'appointments': appointments,
        'success_message': success_message,
        'selected_appointment': selected_appointment,
    })
    
@login_required
def doctor_view_patients(request):
    try:
        doctor = models.Doctor.objects.get(user = request.user)
    except models.Doctor.DoesNotExist:
        return redirect('doctor_LP')
    
    patients = models.Patient.objects.all()
    
    return render(request, 'doctor/doctor_view_patients.html', {
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
    
    return render(request, 'doctor/doctor_view_billing.html', {
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
    
    return render(request, 'doctor/doctor_med_record_management.html', {
        'doctor': doctor,
        'patients': patients,
        'med_records': med_records,
        'success_message': success_message,
        'selected_med_record': selected_med_record,
    })