from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/new/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    # Doctors
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/new/', views.doctor_create, name='doctor_create'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/new/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', views.appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # Medical Records
    path('records/', views.medical_record_list, name='medical_record_list'),
    path('records/new/', views.medical_record_create, name='medical_record_create'),
    path('records/<int:pk>/edit/', views.medical_record_update, name='medical_record_update'),
    path('records/<int:pk>/delete/', views.medical_record_delete, name='medical_record_delete'),

    # Wards
    path('wards/', views.ward_list, name='ward_list'),
    path('wards/new/', views.ward_create, name='ward_create'),
    path('wards/<int:pk>/edit/', views.ward_update, name='ward_update'),

    # Admissions
    path('admissions/', views.admission_list, name='admission_list'),
    path('admissions/new/', views.admission_create, name='admission_create'),
    path('admissions/<int:pk>/edit/', views.admission_update, name='admission_update'),

    # Invoices
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/new/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:pk>/edit/', views.invoice_update, name='invoice_update'),

    # Staff
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/new/', views.staff_create, name='staff_create'),
    path('staff/<int:pk>/edit/', views.staff_update, name='staff_update'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff_delete'),

    # Lab Tests
    path('labs/', views.lab_test_list, name='lab_test_list'),
    path('labs/new/', views.lab_test_create, name='lab_test_create'),
    path('labs/<int:pk>/edit/', views.lab_test_update, name='lab_test_update'),

    # Departments
    path('departments/', views.department_list, name='department_list'),
    path('departments/new/', views.department_create, name='department_create'),
    path('departments/<int:pk>/edit/', views.department_update, name='department_update'),

    # Reports
    path('reports/', views.reports, name='reports'),
]
