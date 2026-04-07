from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    head_doctor = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('General Surgery', 'General Surgery'),
        ('Internal Medicine', 'Internal Medicine'),
        ('Dermatology', 'Dermatology'),
        ('Radiology', 'Radiology'),
        ('Ophthalmology', 'Ophthalmology'),
        ('Gynecology', 'Gynecology'),
        ('ENT', 'ENT'),
        ('Psychiatry', 'Psychiatry'),
        ('Oncology', 'Oncology'),
        ('Urology', 'Urology'),
    ]
    AVAILABLE_DAYS = [
        ('Mon-Fri', 'Monday to Friday'),
        ('Mon-Sat', 'Monday to Saturday'),
        ('Mon-Sun', 'Monday to Sunday'),
        ('Tue-Sat', 'Tuesday to Saturday'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100, choices=SPECIALIZATION_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_days = models.CharField(max_length=50, choices=AVAILABLE_DAYS, default='Mon-Fri')
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='17:00')
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name', 'last_name']


class Patient(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    MARITAL_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')]

    patient_id = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    emergency_contact_relation = models.CharField(max_length=50, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last = Patient.objects.order_by('id').last()
            num = (last.id + 1) if last else 1
            self.patient_id = f'PT{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    class Meta:
        ordering = ['-registered_date']


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-Show', 'No-Show'),
    ]
    TYPE_CHOICES = [
        ('Consultation', 'Consultation'),
        ('Follow-up', 'Follow-up'),
        ('Emergency', 'Emergency'),
        ('Checkup', 'Checkup'),
        ('Procedure', 'Procedure'),
    ]

    appointment_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    symptoms = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            last = Appointment.objects.order_by('id').last()
            num = (last.id + 1) if last else 1
            self.appointment_id = f'APT{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_id} - {self.patient} with {self.doctor}"

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField()
    symptoms = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription = models.TextField(blank=True)
    lab_tests = models.TextField(blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    visit_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record: {self.patient} - {self.visit_date}"

    class Meta:
        ordering = ['-visit_date']


class Ward(models.Model):
    WARD_TYPE_CHOICES = [
        ('General', 'General'),
        ('Private', 'Private'),
        ('ICU', 'ICU'),
        ('Emergency', 'Emergency'),
        ('Pediatric', 'Pediatric'),
        ('Maternity', 'Maternity'),
        ('Surgical', 'Surgical'),
    ]

    name = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    total_beds = models.IntegerField(default=10)
    floor = models.IntegerField(default=1)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.ward_type})"

    @property
    def available_beds(self):
        occupied = self.admissions.filter(status='Admitted').count()
        return self.total_beds - occupied

    class Meta:
        ordering = ['name']


class Admission(models.Model):
    STATUS_CHOICES = [
        ('Admitted', 'Admitted'),
        ('Discharged', 'Discharged'),
        ('Transferred', 'Transferred'),
    ]

    admission_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='admissions')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='admissions')
    bed_number = models.CharField(max_length=10)
    admission_date = models.DateField(default=timezone.now)
    discharge_date = models.DateField(null=True, blank=True)
    reason = models.TextField()
    diagnosis = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Admitted')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.admission_id:
            last = Admission.objects.order_by('id').last()
            num = (last.id + 1) if last else 1
            self.admission_id = f'ADM{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admission_id} - {self.patient}"

    class Meta:
        ordering = ['-admission_date']


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Partially Paid', 'Partially Paid'),
        ('Cancelled', 'Cancelled'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Insurance', 'Insurance'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Online', 'Online'),
    ]

    invoice_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medicine_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    room_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    notes = models.TextField(blank=True)
    invoice_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last = Invoice.objects.order_by('id').last()
            num = (last.id + 1) if last else 1
            self.invoice_id = f'INV{num:05d}'
        subtotal = (self.consultation_fee + self.medicine_charges + self.lab_charges +
                    self.room_charges + self.other_charges)
        self.total_amount = subtotal - self.discount + self.tax
        super().save(*args, **kwargs)

    @property
    def balance(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"{self.invoice_id} - {self.patient}"

    class Meta:
        ordering = ['-invoice_date']


class Staff(models.Model):
    ROLE_CHOICES = [
        ('Nurse', 'Nurse'),
        ('Receptionist', 'Receptionist'),
        ('Lab Technician', 'Lab Technician'),
        ('Pharmacist', 'Pharmacist'),
        ('Administrator', 'Administrator'),
        ('Security', 'Security'),
        ('Cleaner', 'Cleaner'),
        ('Accountant', 'Accountant'),
    ]
    SHIFT_CHOICES = [
        ('Morning', 'Morning (6AM-2PM)'),
        ('Afternoon', 'Afternoon (2PM-10PM)'),
        ('Night', 'Night (10PM-6AM)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, default='Morning')
    joined_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last = Staff.objects.order_by('id').last()
            num = (last.id + 1) if last else 1
            self.employee_id = f'EMP{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name', 'last_name']


class LabTest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    test_id = models.CharField(max_length=20, unique=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_tests')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='lab_tests')
    test_name = models.CharField(max_length=200)
    test_date = models.DateField(default=timezone.now)
    result = models.TextField(blank=True)
    normal_range = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.test_id:
            last = LabTest.objects.order_by('id').last()
            num = (last.id + 1) if last else 1
            self.test_id = f'LAB{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.test_id} - {self.patient} - {self.test_name}"

    class Meta:
        ordering = ['-test_date']
