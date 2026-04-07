#!/usr/bin/env python
"""
Hospital Management System - Quick Setup Script
Run: python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from hospital.models import Department, Doctor, Patient, Appointment, Ward, Staff, Invoice, LabTest
from datetime import date, time, timedelta
from decimal import Decimal


def run():
    print("🏥 MediCare HMS Setup Starting...")

    # ── Superuser ──────────────────────────────────────────────────────────
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@medicare.com', 'admin123')
        print("✅ Superuser created: admin / admin123")
    else:
        print("ℹ️  Superuser already exists")

    # ── Departments ────────────────────────────────────────────────────────
    dept_data = [
        ('Cardiology',      'Heart and cardiovascular diseases',     'Dr. James Wilson',    '+1-555-0101'),
        ('Neurology',       'Brain and nervous system disorders',     'Dr. Sarah Chen',      '+1-555-0102'),
        ('Orthopedics',     'Bone, joint and muscle conditions',      'Dr. Michael Torres',  '+1-555-0103'),
        ('Pediatrics',      'Healthcare for infants and children',    'Dr. Emily Parker',    '+1-555-0104'),
        ('General Surgery', 'Surgical procedures and operations',     'Dr. Robert Singh',    '+1-555-0105'),
        ('Radiology',       'Medical imaging and diagnostics',        'Dr. Lisa Johnson',    '+1-555-0106'),
    ]
    depts = {}
    for name, desc, head, phone in dept_data:
        dept, _ = Department.objects.get_or_create(
            name=name,
            defaults={'description': desc, 'head_doctor': head, 'phone': phone}
        )
        depts[name] = dept
    print(f"✅ {len(dept_data)} departments created")

    # ── Doctors ────────────────────────────────────────────────────────────
    doctor_data = [
        ('James',   'Wilson',  'james.wilson@medicare.com',  '+1-555-1001', 'Cardiology',       'MD-001', 15, Decimal('250.00'), depts['Cardiology']),
        ('Sarah',   'Chen',    'sarah.chen@medicare.com',    '+1-555-1002', 'Neurology',        'MD-002', 12, Decimal('300.00'), depts['Neurology']),
        ('Michael', 'Torres',  'michael.torres@medicare.com','+1-555-1003', 'Orthopedics',      'MD-003', 10, Decimal('200.00'), depts['Orthopedics']),
        ('Emily',   'Parker',  'emily.parker@medicare.com',  '+1-555-1004', 'Pediatrics',       'MD-004',  8, Decimal('180.00'), depts['Pediatrics']),
        ('Robert',  'Singh',   'robert.singh@medicare.com',  '+1-555-1005', 'General Surgery',  'MD-005', 20, Decimal('350.00'), depts['General Surgery']),
        ('Lisa',    'Johnson', 'lisa.johnson@medicare.com',  '+1-555-1006', 'Radiology',        'MD-006',  6, Decimal('150.00'), depts['Radiology']),
    ]
    doctors = []
    for fn, ln, email, phone, spec, lic, exp, fee, dept in doctor_data:
        doc, _ = Doctor.objects.get_or_create(
            license_number=lic,
            defaults={
                'first_name': fn, 'last_name': ln, 'email': email,
                'phone': phone, 'specialization': spec, 'department': dept,
                'experience_years': exp, 'consultation_fee': fee,
                'available_from': time(9, 0), 'available_to': time(17, 0),
            }
        )
        doctors.append(doc)
    print(f"✅ {len(doctor_data)} doctors created")

    # ── Patients ───────────────────────────────────────────────────────────
    patient_data = [
        ('Alice',   'Johnson',  'alice.j@email.com',   '+1-555-2001', date(1985, 3, 15),  'Female', 'A+', 'New York'),
        ('Bob',     'Smith',    'bob.s@email.com',     '+1-555-2002', date(1978, 7, 22),  'Male',   'O-', 'Los Angeles'),
        ('Carol',   'Williams', 'carol.w@email.com',   '+1-555-2003', date(1992, 11, 8),  'Female', 'B+', 'Chicago'),
        ('David',   'Brown',    'david.b@email.com',   '+1-555-2004', date(1965, 1, 30),  'Male',   'AB+','Houston'),
        ('Eva',     'Davis',    'eva.d@email.com',     '+1-555-2005', date(2000, 5, 19),  'Female', 'O+', 'Phoenix'),
        ('Frank',   'Miller',   'frank.m@email.com',   '+1-555-2006', date(1955, 9, 3),   'Male',   'A-', 'Philadelphia'),
        ('Grace',   'Wilson',   'grace.w@email.com',   '+1-555-2007', date(1990, 12, 25), 'Female', 'B-', 'San Antonio'),
        ('Henry',   'Moore',    'henry.m@email.com',   '+1-555-2008', date(1972, 4, 14),  'Male',   'AB-','San Diego'),
    ]
    patients = []
    for fn, ln, email, phone, dob, gender, bg, city in patient_data:
        pat, _ = Patient.objects.get_or_create(
            email=email,
            defaults={
                'first_name': fn, 'last_name': ln, 'phone': phone,
                'date_of_birth': dob, 'gender': gender, 'blood_group': bg,
                'city': city, 'emergency_contact_name': 'Emergency Contact',
                'emergency_contact_phone': '+1-555-9999',
            }
        )
        patients.append(pat)
    print(f"✅ {len(patient_data)} patients created")

    # ── Appointments ───────────────────────────────────────────────────────
    today = date.today()
    apt_data = [
        (patients[0], doctors[0], today,               time(9,  0),  'Consultation', 'Scheduled'),
        (patients[1], doctors[1], today,               time(10, 30), 'Follow-up',    'Confirmed'),
        (patients[2], doctors[2], today + timedelta(1),time(11, 0),  'Checkup',      'Scheduled'),
        (patients[3], doctors[3], today + timedelta(2),time(14, 0),  'Consultation', 'Scheduled'),
        (patients[4], doctors[4], today - timedelta(1),time(9,  30), 'Procedure',    'Completed'),
        (patients[5], doctors[5], today - timedelta(2),time(15, 0),  'Consultation', 'Completed'),
        (patients[6], doctors[0], today + timedelta(3),time(10, 0),  'Follow-up',    'Scheduled'),
        (patients[7], doctors[1], today - timedelta(3),time(13, 0),  'Checkup',      'Completed'),
    ]
    for pat, doc, apd, apt, atype, status in apt_data:
        Appointment.objects.get_or_create(
            patient=pat, doctor=doc, appointment_date=apd, appointment_time=apt,
            defaults={'appointment_type': atype, 'status': status, 'symptoms': 'Routine check'}
        )
    print(f"✅ {len(apt_data)} appointments created")

    # ── Wards ──────────────────────────────────────────────────────────────
    ward_data = [
        ('General Ward A',  'General', depts['General Surgery'], 20, 1),
        ('Cardiology ICU',  'ICU',     depts['Cardiology'],      10, 2),
        ('Pediatric Ward',  'Pediatric', depts['Pediatrics'],    15, 2),
        ('Private Suite',   'Private', depts['General Surgery'],  8, 3),
        ('Emergency Ward',  'Emergency', depts['General Surgery'],12, 1),
    ]
    for name, wtype, dept, beds, floor in ward_data:
        Ward.objects.get_or_create(
            name=name,
            defaults={'ward_type': wtype, 'department': dept, 'total_beds': beds, 'floor': floor}
        )
    print(f"✅ {len(ward_data)} wards created")

    # ── Staff ──────────────────────────────────────────────────────────────
    staff_data = [
        ('Nancy', 'Green',  'nancy.g@medicare.com',  '+1-555-3001', 'Nurse',         depts['Cardiology'],      Decimal('55000'), 'Morning'),
        ('Peter', 'White',  'peter.w@medicare.com',  '+1-555-3002', 'Receptionist',  depts['General Surgery'], Decimal('40000'), 'Morning'),
        ('Quinn', 'Black',  'quinn.b@medicare.com',  '+1-555-3003', 'Lab Technician',depts['Radiology'],       Decimal('50000'), 'Afternoon'),
        ('Rachel','Taylor', 'rachel.t@medicare.com', '+1-555-3004', 'Pharmacist',    depts['General Surgery'], Decimal('65000'), 'Morning'),
    ]
    for fn, ln, email, phone, role, dept, salary, shift in staff_data:
        Staff.objects.get_or_create(
            email=email,
            defaults={'first_name': fn, 'last_name': ln, 'phone': phone, 'role': role,
                      'department': dept, 'salary': salary, 'shift': shift}
        )
    print(f"✅ {len(staff_data)} staff created")

    # ── Invoices ───────────────────────────────────────────────────────────
    invoice_data = [
        (patients[4], Decimal('350'), Decimal('50'), Decimal('120'), Decimal('0'), 'Paid',    'Cash'),
        (patients[5], Decimal('150'), Decimal('0'),  Decimal('80'),  Decimal('0'), 'Paid',    'Card'),
        (patients[7], Decimal('300'), Decimal('75'), Decimal('0'),   Decimal('0'), 'Paid',    'Insurance'),
        (patients[0], Decimal('250'), Decimal('30'), Decimal('90'),  Decimal('0'), 'Pending', ''),
        (patients[1], Decimal('300'), Decimal('60'), Decimal('150'), Decimal('0'), 'Pending', ''),
    ]
    for pat, consult, med, lab, disc, status, method in invoice_data:
        inv, created = Invoice.objects.get_or_create(
            patient=pat, status=status,
            defaults={
                'consultation_fee': consult, 'medicine_charges': med,
                'lab_charges': lab, 'discount': disc, 'status': status,
                'payment_method': method,
                'paid_amount': (consult + med + lab - disc) if status == 'Paid' else Decimal('0'),
                'invoice_date': today - timedelta(days=5),
            }
        )
    print(f"✅ {len(invoice_data)} invoices created")

    # ── Lab Tests ──────────────────────────────────────────────────────────
    lab_data = [
        (patients[0], doctors[0], 'Complete Blood Count (CBC)',        today,               'Pending',    Decimal('45')),
        (patients[1], doctors[1], 'MRI Brain Scan',                    today - timedelta(1),'Completed',  Decimal('350')),
        (patients[2], doctors[2], 'X-Ray Right Knee',                  today - timedelta(1),'Completed',  Decimal('80')),
        (patients[3], doctors[3], 'Echocardiogram',                    today,               'In Progress',Decimal('220')),
        (patients[4], doctors[4], 'Urinalysis',                        today - timedelta(2),'Completed',  Decimal('35')),
    ]
    for pat, doc, name, tdate, status, cost in lab_data:
        LabTest.objects.get_or_create(
            patient=pat, test_name=name,
            defaults={'doctor': doc, 'test_date': tdate, 'status': status, 'cost': cost}
        )
    print(f"✅ {len(lab_data)} lab tests created")

    print("\n" + "="*50)
    print("🎉  Setup Complete!")
    print("="*50)
    print("   URL:      http://127.0.0.1:8000/")
    print("   Admin:    http://127.0.0.1:8000/admin/")
    print("   Username: admin")
    print("   Password: admin123")
    print("="*50)


if __name__ == '__main__':
    run()
