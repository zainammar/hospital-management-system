from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, timedelta
from .models import (Doctor, Patient, Appointment, MedicalRecord,
                     Ward, Admission, Invoice, Staff, LabTest, Department)
from .forms import (DoctorForm, PatientForm, AppointmentForm, MedicalRecordForm,
                    WardForm, AdmissionForm, InvoiceForm, StaffForm, LabTestForm, DepartmentForm)


@login_required
def dashboard(request):
    today = date.today()
    stats = {
        'total_patients': Patient.objects.filter(is_active=True).count(),
        'total_doctors': Doctor.objects.filter(is_active=True).count(),
        'total_staff': Staff.objects.filter(is_active=True).count(),
        'today_appointments': Appointment.objects.filter(appointment_date=today).count(),
        'pending_appointments': Appointment.objects.filter(status='Scheduled').count(),
        'admitted_patients': Admission.objects.filter(status='Admitted').count(),
        'pending_invoices': Invoice.objects.filter(status='Pending').count(),
        'pending_labs': LabTest.objects.filter(status='Pending').count(),
        'total_revenue': Invoice.objects.filter(status='Paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'monthly_revenue': Invoice.objects.filter(
            status='Paid', invoice_date__month=today.month
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
    }
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]
    recent_patients = Patient.objects.order_by('-registered_date')[:5]
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=today, status__in=['Scheduled', 'Confirmed']
    ).select_related('patient', 'doctor').order_by('appointment_date', 'appointment_time')[:5]
    departments = Department.objects.annotate(doctor_count=Count('doctor')).all()

    context = {
        **stats,
        'recent_appointments': recent_appointments,
        'recent_patients': recent_patients,
        'upcoming_appointments': upcoming_appointments,
        'departments': departments,
    }
    return render(request, 'hospital/dashboard.html', context)


# ==================== PATIENT VIEWS ====================
@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(is_active=True)
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(patient_id__icontains=query) | Q(phone__icontains=query)
        )
    return render(request, 'hospital/patient_list.html', {'patients': patients, 'query': query})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.select_related('doctor').order_by('-appointment_date')[:5]
    medical_records = patient.medical_records.select_related('doctor').order_by('-visit_date')[:5]
    admissions = patient.admissions.select_related('doctor', 'ward').order_by('-admission_date')[:3]
    invoices = patient.invoices.order_by('-invoice_date')[:5]
    lab_tests = patient.lab_tests.select_related('doctor').order_by('-test_date')[:5]
    return render(request, 'hospital/patient_detail.html', {
        'patient': patient, 'appointments': appointments,
        'medical_records': medical_records, 'admissions': admissions,
        'invoices': invoices, 'lab_tests': lab_tests,
    })


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.full_name} registered successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    return render(request, 'hospital/patient_form.html', {'form': form, 'title': 'Register New Patient'})


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'hospital/patient_form.html', {'form': form, 'title': 'Update Patient', 'patient': patient})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.is_active = False
        patient.save()
        messages.success(request, 'Patient deactivated successfully!')
        return redirect('patient_list')
    return render(request, 'hospital/confirm_delete.html', {'object': patient, 'type': 'Patient'})


# ==================== DOCTOR VIEWS ====================
@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    doctors = Doctor.objects.filter(is_active=True).select_related('department')
    if query:
        doctors = doctors.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    return render(request, 'hospital/doctor_list.html', {'doctors': doctors, 'query': query})


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    appointments = doctor.appointments.select_related('patient').order_by('-appointment_date')[:5]
    return render(request, 'hospital/doctor_detail.html', {'doctor': doctor, 'appointments': appointments})


@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            messages.success(request, f'{doctor.full_name} added successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm()
    return render(request, 'hospital/doctor_form.html', {'form': form, 'title': 'Add New Doctor'})


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully!')
            return redirect('doctor_detail', pk=doctor.pk)
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'hospital/doctor_form.html', {'form': form, 'title': 'Update Doctor', 'doctor': doctor})


@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.is_active = False
        doctor.save()
        messages.success(request, 'Doctor deactivated successfully!')
        return redirect('doctor_list')
    return render(request, 'hospital/confirm_delete.html', {'object': doctor, 'type': 'Doctor'})


# ==================== APPOINTMENT VIEWS ====================
@login_required
def appointment_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    if query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=query) | Q(patient__last_name__icontains=query) |
            Q(appointment_id__icontains=query) | Q(doctor__first_name__icontains=query)
        )
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'hospital/appointment_list.html', {
        'appointments': appointments, 'query': query, 'status_filter': status_filter
    })


@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            apt = form.save()
            messages.success(request, f'Appointment {apt.appointment_id} created!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'hospital/appointment_form.html', {'form': form, 'title': 'Schedule Appointment'})


@login_required
def appointment_update(request, pk):
    apt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=apt)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated!')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=apt)
    return render(request, 'hospital/appointment_form.html', {'form': form, 'title': 'Update Appointment', 'apt': apt})


@login_required
def appointment_delete(request, pk):
    apt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        apt.delete()
        messages.success(request, 'Appointment deleted!')
        return redirect('appointment_list')
    return render(request, 'hospital/confirm_delete.html', {'object': apt, 'type': 'Appointment'})


# ==================== MEDICAL RECORD VIEWS ====================
@login_required
def medical_record_list(request):
    query = request.GET.get('q', '')
    records = MedicalRecord.objects.select_related('patient', 'doctor').all()
    if query:
        records = records.filter(
            Q(patient__first_name__icontains=query) | Q(patient__last_name__icontains=query) |
            Q(diagnosis__icontains=query)
        )
    return render(request, 'hospital/medical_record_list.html', {'records': records, 'query': query})


@login_required
def medical_record_create(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical record created!')
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm()
    return render(request, 'hospital/medical_record_form.html', {'form': form, 'title': 'Add Medical Record'})


@login_required
def medical_record_update(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical record updated!')
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm(instance=record)
    return render(request, 'hospital/medical_record_form.html', {'form': form, 'title': 'Update Medical Record'})


@login_required
def medical_record_delete(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Medical record deleted!')
        return redirect('medical_record_list')
    return render(request, 'hospital/confirm_delete.html', {'object': record, 'type': 'Medical Record'})


# ==================== WARD VIEWS ====================
@login_required
def ward_list(request):
    wards = Ward.objects.filter(is_active=True).select_related('department')
    return render(request, 'hospital/ward_list.html', {'wards': wards})


@login_required
def ward_create(request):
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ward created!')
            return redirect('ward_list')
    else:
        form = WardForm()
    return render(request, 'hospital/ward_form.html', {'form': form, 'title': 'Add Ward'})


@login_required
def ward_update(request, pk):
    ward = get_object_or_404(Ward, pk=pk)
    if request.method == 'POST':
        form = WardForm(request.POST, instance=ward)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ward updated!')
            return redirect('ward_list')
    else:
        form = WardForm(instance=ward)
    return render(request, 'hospital/ward_form.html', {'form': form, 'title': 'Update Ward', 'ward': ward})


# ==================== ADMISSION VIEWS ====================
@login_required
def admission_list(request):
    admissions = Admission.objects.select_related('patient', 'doctor', 'ward').all()
    return render(request, 'hospital/admission_list.html', {'admissions': admissions})


@login_required
def admission_create(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            adm = form.save()
            messages.success(request, f'Admission {adm.admission_id} created!')
            return redirect('admission_list')
    else:
        form = AdmissionForm()
    return render(request, 'hospital/admission_form.html', {'form': form, 'title': 'New Admission'})


@login_required
def admission_update(request, pk):
    adm = get_object_or_404(Admission, pk=pk)
    if request.method == 'POST':
        form = AdmissionForm(request.POST, instance=adm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admission updated!')
            return redirect('admission_list')
    else:
        form = AdmissionForm(instance=adm)
    return render(request, 'hospital/admission_form.html', {'form': form, 'title': 'Update Admission', 'adm': adm})


# ==================== INVOICE VIEWS ====================
@login_required
def invoice_list(request):
    query = request.GET.get('q', '')
    invoices = Invoice.objects.select_related('patient').all()
    if query:
        invoices = invoices.filter(
            Q(patient__first_name__icontains=query) | Q(invoice_id__icontains=query)
        )
    return render(request, 'hospital/invoice_list.html', {'invoices': invoices, 'query': query})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'hospital/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            inv = form.save()
            messages.success(request, f'Invoice {inv.invoice_id} created!')
            return redirect('invoice_detail', pk=inv.pk)
    else:
        form = InvoiceForm()
    return render(request, 'hospital/invoice_form.html', {'form': form, 'title': 'Create Invoice'})


@login_required
def invoice_update(request, pk):
    inv = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=inv)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated!')
            return redirect('invoice_detail', pk=inv.pk)
    else:
        form = InvoiceForm(instance=inv)
    return render(request, 'hospital/invoice_form.html', {'form': form, 'title': 'Update Invoice', 'inv': inv})


# ==================== STAFF VIEWS ====================
@login_required
def staff_list(request):
    query = request.GET.get('q', '')
    staff = Staff.objects.filter(is_active=True).select_related('department')
    if query:
        staff = staff.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |
            Q(role__icontains=query) | Q(employee_id__icontains=query)
        )
    return render(request, 'hospital/staff_list.html', {'staff': staff, 'query': query})


@login_required
def staff_create(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            s = form.save()
            messages.success(request, f'Staff {s.full_name} added!')
            return redirect('staff_list')
    else:
        form = StaffForm()
    return render(request, 'hospital/staff_form.html', {'form': form, 'title': 'Add Staff Member'})


@login_required
def staff_update(request, pk):
    s = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=s)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated!')
            return redirect('staff_list')
    else:
        form = StaffForm(instance=s)
    return render(request, 'hospital/staff_form.html', {'form': form, 'title': 'Update Staff', 'staff': s})


@login_required
def staff_delete(request, pk):
    s = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        s.is_active = False
        s.save()
        messages.success(request, 'Staff deactivated!')
        return redirect('staff_list')
    return render(request, 'hospital/confirm_delete.html', {'object': s, 'type': 'Staff Member'})


# ==================== LAB TEST VIEWS ====================
@login_required
def lab_test_list(request):
    query = request.GET.get('q', '')
    tests = LabTest.objects.select_related('patient', 'doctor').all()
    if query:
        tests = tests.filter(
            Q(patient__first_name__icontains=query) | Q(test_name__icontains=query) |
            Q(test_id__icontains=query)
        )
    return render(request, 'hospital/lab_test_list.html', {'tests': tests, 'query': query})


@login_required
def lab_test_create(request):
    if request.method == 'POST':
        form = LabTestForm(request.POST)
        if form.is_valid():
            t = form.save()
            messages.success(request, f'Lab test {t.test_id} created!')
            return redirect('lab_test_list')
    else:
        form = LabTestForm()
    return render(request, 'hospital/lab_test_form.html', {'form': form, 'title': 'New Lab Test'})


@login_required
def lab_test_update(request, pk):
    test = get_object_or_404(LabTest, pk=pk)
    if request.method == 'POST':
        form = LabTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lab test updated!')
            return redirect('lab_test_list')
    else:
        form = LabTestForm(instance=test)
    return render(request, 'hospital/lab_test_form.html', {'form': form, 'title': 'Update Lab Test', 'test': test})


# ==================== DEPARTMENT VIEWS ====================
@login_required
def department_list(request):
    departments = Department.objects.annotate(
        doctor_count=Count('doctor'),
        staff_count=Count('staff')
    ).all()
    return render(request, 'hospital/department_list.html', {'departments': departments})


@login_required
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hospital/department_form.html', {'form': form, 'title': 'Add Department'})


@login_required
def department_update(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated!')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)
    return render(request, 'hospital/department_form.html', {'form': form, 'title': 'Update Department', 'dept': dept})


@login_required
def reports(request):
    today = date.today()
    month_start = today.replace(day=1)

    monthly_appointments = Appointment.objects.filter(
        appointment_date__gte=month_start
    ).count()

    revenue_by_month = []
    for i in range(6):
        month = today.replace(day=1) - timedelta(days=i * 30)
        rev = Invoice.objects.filter(
            status='Paid',
            invoice_date__year=month.year,
            invoice_date__month=month.month
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        revenue_by_month.append({'month': month.strftime('%b %Y'), 'revenue': float(rev)})

    top_doctors = Doctor.objects.annotate(
        appt_count=Count('appointments')
    ).order_by('-appt_count')[:5]

    dept_stats = Department.objects.annotate(
        doctor_count=Count('doctor'),
        patient_count=Count('doctor__appointments__patient', distinct=True)
    ).all()

    context = {
        'monthly_appointments': monthly_appointments,
        'revenue_by_month': revenue_by_month,
        'top_doctors': top_doctors,
        'dept_stats': dept_stats,
        'total_revenue': Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
    }
    return render(request, 'hospital/reports.html', context)
