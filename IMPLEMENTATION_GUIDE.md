# IMPLEMENTATION_GUIDE.md

# Implementation Guide - SPP Management System

Panduan lengkap untuk mengimplementasikan Sistem Manajemen SPP sesuai modul MINGGU 11.

## 📋 Daftar Isi

1. [Struktur Direktori](#struktur-direktori)
2. [Step-by-Step Implementation](#step-by-step-implementation)
3. [Contoh Penggunaan](#contoh-penggunaan)
4. [Troubleshooting](#troubleshooting)

## 📁 Struktur Direktori

```
MODUL_SPP/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Konfigurasi aplikasi
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py           # Model Student & ProgramStudi
│   │   ├── billing.py           # Model Billing & Semester
│   │   ├── payment.py           # Model Payment & PaymentReconciliation
│   │   └── payment_method.py    # Model PaymentMethod
│   ├── services/
│   │   ├── __init__.py
│   │   ├── billing_service.py   # Business logic untuk billing
│   │   ├── payment_service.py   # Business logic untuk payment
│   │   └── ai_service.py        # AI insights & reporting
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── billing_routes.py    # API endpoints untuk billing
│   │   ├── payment_routes.py    # API endpoints untuk payment
│   │   ├── webhook_routes.py    # Webhook handler
│   │   └── dashboard_routes.py  # Dashboard & analytics
│   ├── schedulers/
│   │   ├── __init__.py
│   │   └── billing_scheduler.py # APScheduler untuk billing otomatis
│   └── utils/
│       ├── __init__.py
│       ├── logger.py            # Logging configuration
│       └── decorators.py        # Custom decorators
├── tests/
│   ├── test_billing_service.py
│   └── test_payment_service.py
├── static/              # Frontend assets (optional)
├── logs/               # Log files
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md          # Dokumentasi

```

## 🚀 Step-by-Step Implementation

### Step 1: Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup

```bash
# Jalankan aplikasi untuk membuat database
python app.py

# Database akan otomatis dibuat dengan sample data:
# - 4 Program Studi
# - 4 Payment Methods
# - File: spp_management.db
```

### Step 3: Verify Installation

```bash
# Test API - Health check
curl http://localhost:5000/health

# Expected response:
# {
#     "status": "healthy",
#     "service": "SPP Management System",
#     "timestamp": "2024-01-15T10:30:00"
# }
```

### Step 4: Create Sample Data

```bash
# Buka Python shell
python

# Jalankan kode berikut:
from app import create_app, db
from app.models.student import Student, ProgramStudi
from app.models.billing import Billing, Semester
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    # Get existing program studi
    ti = ProgramStudi.query.filter_by(code='TI').first()
    
    # Create students
    for i in range(5):
        student = Student(
            nim=f'2021000{i:02d}',
            name=f'Student {i+1}',
            email=f'student{i+1}@university.edu',
            program_studi_id=ti.id,
            status='active'
        )
        db.session.add(student)
    
    db.session.commit()
    print("✅ Sample students created")
```

### Step 5: Generate Billing

```bash
# Buka Python shell
python

from app import create_app, db
from app.models.billing import Semester
from app.services.billing_service import BillingService
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    # Create semester
    semester = Semester(
        name='2024/2025-Ganjil',
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=120),
        is_active=True
    )
    db.session.add(semester)
    db.session.commit()
    
    # Generate billing
    billing_service = BillingService()
    result = billing_service.generate_billing_for_semester(semester.id)
    print(f"✅ {result['message']}")
```

## 💡 Contoh Penggunaan

### Use Case 1: Create Billing & Track Payment

```python
# Scenario: Generate billing untuk semester baru

from app import create_app, db
from app.models.billing import Semester, Billing
from app.models.student import Student
from app.services.billing_service import BillingService
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Step 1: Create semester
    semester = Semester(
        name='2024/2025-Ganjil',
        start_date=datetime.utcnow(),
        end_date=datetime.utcnow() + timedelta(days=120),
        is_active=True
    )
    db.session.add(semester)
    db.session.commit()
    
    # Step 2: Generate billing
    billing_service = BillingService()
    result = billing_service.generate_billing_for_semester(semester.id)
    
    print(f"Generated billings: {result['created_count']}")
    
    # Step 3: Check student billing
    student = Student.query.filter_by(nim='2021000001').first()
    summary = billing_service.get_billing_summary(student.id)
    
    print(f"Student: {summary['student'].name}")
    print(f"Total Billed: Rp {summary['total_billed']:,}")
    print(f"Total Paid: Rp {summary['total_paid']:,}")
    print(f"Outstanding: Rp {summary['total_outstanding']:,}")
```

### Use Case 2: Process Payment

```python
# Scenario: Mahasiswa melakukan pembayaran

from app import create_app, db
from app.models.payment_method import PaymentMethod
from app.models.billing import Billing
from app.services.payment_service import PaymentService

app = create_app()

with app.app_context():
    # Step 1: Get billing
    billing = Billing.query.filter_by(status='unpaid').first()
    
    # Step 2: Get payment method (e.g., BCA Virtual Account)
    payment_method = PaymentMethod.query.filter_by(
        gateway_code='bca_virtual'
    ).first()
    
    # Step 3: Process payment
    payment_service = PaymentService()
    result = payment_service.process_payment(
        billing_id=billing.id,
        amount=5000000,
        payment_method_id=payment_method.id,
        transaction_id='TXN20240115001',
        gateway_name='bca_virtual'
    )
    
    if result['success']:
        print(f"✅ Payment processed: {result['payment'].reference_code}")
        print(f"📊 Billing Status: {result['billing'].status}")
    else:
        print(f"❌ Payment failed: {result['message']}")
```

### Use Case 3: Check KRS Eligibility

```python
# Scenario: Mahasiswa ingin mendaftar KRS tapi ada tunggakan

from app import create_app, db
from app.models.student import Student
from app.services.billing_service import BillingService

app = create_app()

with app.app_context():
    student = Student.query.filter_by(nim='2021000001').first()
    
    billing_service = BillingService()
    result = billing_service.can_student_register_krs(student.id)
    
    if result['can_register']:
        print(f"✅ {result['message']}")
        print("📋 Silakan mendaftar KRS")
    else:
        print(f"❌ {result['message']}")
        print(f"💰 Lunasi tunggakan: Rp {result['outstanding']:,}")
```

### Use Case 4: Generate Financial Report

```python
# Scenario: Membuat laporan keuangan bulanan

from app import create_app, db
from app.services.ai_service import AIFinancialService
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    ai_service = AIFinancialService()
    
    # Get report for last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    report = ai_service.generate_financial_report(start_date)
    
    print(f"📊 Financial Report")
    print(f"Period: {start_date.date()} - {datetime.utcnow().date()}")
    print(f"Total Revenue: Rp {report['revenue_metrics']['total_revenue']:,}")
    print(f"Collection Rate: {report['revenue_metrics']['collection_rate']}%")
    print(f"\n🤖 AI Insights:")
    for insight in report['ai_insights']['insights']:
        print(f"  {insight}")
    print(f"\n📋 Recommendations:")
    for rec in report['ai_insights']['recommendations']:
        print(f"  • {rec}")
```

### Use Case 5: Handle Webhook

```bash
# Scenario: Payment gateway mengirim webhook notifikasi

# Test webhook dengan curl:
curl -X POST http://localhost:5000/api/webhook/payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN20240115001",
    "reference_code": "PAY20240115123456ABC",
    "amount": 5000000,
    "status": "success",
    "timestamp": "2024-01-15T10:30:00",
    "signature": "HMAC_SHA256_SIGNATURE"
  }'

# Expected response:
# {
#     "success": true,
#     "message": "Webhook processed successfully"
# }
```

## 🔧 Customization

### Change Penalty Configuration

```python
# app/config.py
OVERDUE_PENALTY_PER_DAY = 15000  # Ganti dari 10000 ke 15000
OVERDUE_MAX_PENALTY = 750000     # Ganti dari 500000 ke 750000
```

### Add New Program Studi

```python
from app import create_app, db
from app.models.student import ProgramStudi

app = create_app()

with app.app_context():
    new_ps = ProgramStudi(
        name='Administrasi Bisnis',
        code='AB',
        spp_amount=3800000
    )
    db.session.add(new_ps)
    db.session.commit()
    print("✅ New program studi added")
```

### Add New Payment Method

```python
from app import create_app, db
from app.models.payment_method import PaymentMethod

app = create_app()

with app.app_context():
    new_pm = PaymentMethod(
        name='Mandiri Transfer',
        method_type='bank_transfer',
        provider='Mandiri',
        gateway_code='mandiri_transfer',
        description='Pembayaran via transfer Mandiri'
    )
    db.session.add(new_pm)
    db.session.commit()
    print("✅ New payment method added")
```

## 🐛 Troubleshooting

### Issue 1: Database Lock Error

```
sqlite3.OperationalError: database is locked
```

**Solution**:
```bash
# Hapus database lama
rm spp_management.db

# Jalankan aplikasi ulang
python app.py
```

### Issue 2: Import Error

```
ModuleNotFoundError: No module named 'app'
```

**Solution**:
```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/MODUL_SPP"

# atau jalankan dari directory yang benar
cd /path/to/MODUL_SPP
python app.py
```

### Issue 3: Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solution**:
```bash
# Kill process yang menggunakan port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :5000
kill -9 <PID>

# atau gunakan port berbeda
python app.py --port 5001
```

### Issue 4: Scheduler Not Running

```python
# Check if scheduler is running
from app.schedulers import scheduler

if scheduler.running:
    print("✅ Scheduler is running")
    print("Jobs:", scheduler.get_jobs())
else:
    print("❌ Scheduler is not running")
```

**Solution**:
```python
# Restart scheduler
from app.schedulers.billing_scheduler import setup_billing_scheduler
from app import create_app

app = create_app()
setup_billing_scheduler(app)
print("✅ Scheduler restarted")
```

## 📞 Support

Untuk pertanyaan atau issues, silakan:
1. Check README.md dan IMPLEMENTATION_GUIDE.md
2. Review error logs di `logs/` directory
3. Run unit tests: `python -m pytest tests/`

## 🎯 Next Steps

Setelah implementasi dasar:
1. **Frontend Development**: Buat dashboard menggunakan React/Vue
2. **Email Integration**: Implementasikan email reminder
3. **Real Payment Gateway**: Integrasikan dengan Midtrans, BCA, dll
4. **Admin Panel**: Buat admin interface untuk management
5. **Reporting**: Export laporan ke PDF/Excel
6. **Mobile App**: Buat mobile app untuk mahasiswa

---

Last Updated: January 15, 2024
Version: 1.0.0
