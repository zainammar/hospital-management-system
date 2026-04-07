from django.contrib import admin
from .models import (Department, Doctor, Patient, Appointment, MedicalRecord,
                     Ward, Admission, Invoice, Staff, LabTest)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head_doctor', 'phone']
    search_fields = ['name']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'department', 'license_number', 'is_active']
    list_filter = ['specialization', 'is_active', 'department']
    search_fields = ['first_name', 'last_name', 'license_number']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'gender', 'blood_group', 'phone', 'registered_date']
    list_filter = ['gender', 'blood_group']
    search_fields = ['first_name', 'last_name', 'patient_id', 'phone']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['appointment_id', 'patient', 'doctor', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_type']
    search_fields = ['appointment_id', 'patient__first_name', 'doctor__first_name']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis']
    search_fields = ['patient__first_name', 'diagnosis']

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'ward_type', 'total_beds', 'available_beds', 'is_active']

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['admission_id', 'patient', 'ward', 'admission_date', 'status']
    list_filter = ['status']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'patient', 'total_amount', 'status', 'invoice_date']
    list_filter = ['status']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'role', 'department', 'is_active']
    list_filter = ['role', 'is_active']

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['test_id', 'patient', 'test_name', 'status', 'test_date']
    list_filter = ['status']
