# 🏥 MediCare — Hospital Management System

A full-featured Hospital Management System built with **Python Django**, featuring a modern dark-sidebar UI, complete CRUD operations across all core hospital modules, and a ready-to-use demo data seeder.

---

## 📋 Features

| Module | Description |
|---|---|
| 🧑‍⚕️ **Patient Management** | Register, view, update patients with complete profiles |
| 👨‍⚕️ **Doctor Management** | Doctor profiles, specializations, availability |
| 📅 **Appointments** | Schedule and track appointments with status management |
| 📁 **Medical Records** | Diagnoses, prescriptions, treatments, follow-ups |
| 🏨 **Ward & Admissions** | Bed management, ward capacity, patient admissions |
| 💰 **Billing & Invoices** | Detailed invoices with charge breakdown and payment tracking |
| 🧪 **Lab Tests** | Order and manage lab tests with results |
| 👥 **Staff Management** | Non-doctor staff with roles and shifts |
| 🏢 **Departments** | Hospital departments with doctor assignment |
| 📊 **Reports** | Revenue charts, top doctors, department stats |
| 🔒 **Authentication** | Login/logout with session management |
| 🛠️ **Django Admin** | Full admin panel for all models |

---

## 🚀 Quick Start

### 1. Clone / Extract the project
```bash
cd hospital_management
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed demo data (creates admin + sample records)
```bash
python setup_demo.py
```

### 6. Start the development server
```bash
python manage.py runserver
```

### 7. Open in browser
```
http://127.0.0.1:8000/
Username: admin
Password: admin123
```

---

## 🗂️ Project Structure

```
hospital_management/
├── hospital_management/        # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── hospital/                   # Main application
│   ├── models.py               # All database models
│   ├── views.py                # All view functions
│   ├── forms.py                # All ModelForms
│   ├── urls.py                 # URL routing
│   └── admin.py                # Admin registrations
├── templates/
│   ├── hospital/               # All HTML templates
│   │   ├── base.html           # Sidebar layout base
│   │   ├── dashboard.html
│   │   ├── patient_*.html
│   │   ├── doctor_*.html
│   │   ├── appointment_*.html
│   │   ├── medical_record_*.html
│   │   ├── ward_*.html
│   │   ├── admission_*.html
│   │   ├── invoice_*.html
│   │   ├── staff_*.html
│   │   ├── lab_test_*.html
│   │   ├── department_*.html
│   │   ├── reports.html
│   │   └── confirm_delete.html
│   └── registration/
│       └── login.html
├── manage.py
├── setup_demo.py               # Demo data seeder
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Models

### Patient
- Personal info (name, DOB, gender, blood group)
- Contact & address details
- Emergency contact
- Insurance info
- Medical history & allergies
- Auto-generated Patient ID (PT00001)

### Doctor
- Professional info (specialization, license, experience)
- Department assignment
- Consultation fee & availability schedule

### Appointment
- Links Patient + Doctor
- Date, time, type, status
- Symptoms and notes
- Auto-generated Appointment ID (APT00001)

### Medical Record
- Linked to appointment
- Diagnosis, treatment, prescription
- Lab test orders, follow-up date

### Ward
- Ward type (General, ICU, Private, etc.)
- Bed count with live available-beds calculation

### Admission
- Patient admission to ward/bed
- Admission and discharge dates
- Status tracking (Admitted/Discharged/Transferred)

### Invoice
- Itemized charges (consultation, medicine, lab, room)
- Discount, tax, paid amount, balance
- Payment method and status

### Staff
- Non-doctor employees (Nurses, Receptionists, etc.)
- Role, shift, salary
- Auto-generated Employee ID (EMP00001)

### Lab Test
- Ordered by doctor for patient
- Result, normal range, status
- Auto-generated Test ID (LAB00001)

---

## 🔧 Configuration

Edit `hospital_management/settings.py` to:
- Change the database (SQLite by default → PostgreSQL/MySQL for production)
- Set `DEBUG = False` for production
- Configure `ALLOWED_HOSTS`
- Add email settings for notifications

### Example: Switch to PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hospital_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Then install: `pip install psycopg2-binary`

---

## 🎨 Tech Stack

- **Backend:** Python 3.10+ / Django 4.2
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Frontend:** Bootstrap 5.3, Bootstrap Icons
- **Charts:** Chart.js 4.4
- **Fonts:** Google Fonts (Plus Jakarta Sans, JetBrains Mono)

---

## 📌 URLs Reference

| URL | Page |
|---|---|
| `/` or `/dashboard/` | Main Dashboard |
| `/patients/` | Patient List |
| `/doctors/` | Doctor List |
| `/appointments/` | Appointment List |
| `/records/` | Medical Records |
| `/wards/` | Ward Management |
| `/admissions/` | Admissions |
| `/invoices/` | Billing & Invoices |
| `/staff/` | Staff Management |
| `/labs/` | Lab Tests |
| `/departments/` | Departments |
| `/reports/` | Reports & Analytics |
| `/admin/` | Django Admin Panel |
| `/login/` | Login Page |

---

## 🔐 Default Credentials

| Role | Username | Password |
|---|---|---|
| Superuser | `admin` | `admin123` |

> ⚠️ Change the default password before deploying to production!

---

## 📄 License

MIT License — free to use, modify, and distribute.
# hospital-management-system
