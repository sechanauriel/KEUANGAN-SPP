# README.md

# SPP Management System - MINGGU 11: Modul Keuangan

Sistem manajemen pembayaran SPP dengan status tunggakan, reminder otomatis, dan integrasi payment gateway. Aplikasi ini dilengkapi dengan AI untuk generate laporan keuangan dan insights.

## 📋 Fitur Utama

### 1. Payment Schema (25%)
- **Tabel Billing**: Menyimpan data tagihan SPP per semester
  - Status: unpaid, partial, paid, overdue
  - Tracking pembayaran dan denda keterlambatan
  
- **Tabel Payment**: Mencatat setiap transaksi pembayaran
  - Reference code unik untuk tracking
  - Status pembayaran (pending, confirmed, failed)
  - Integrasi dengan payment gateway

- **Tabel Payment Method**: Metode pembayaran yang tersedia
  - Bank Transfer
  - Virtual Account
  - E-Wallet (GCash, dll)
  - Credit Card

### 2. Billing Service (35%)
- **Generate Tagihan Otomatis**: Cron job APScheduler membuat billing di awal semester
- **Record Pembayaran**: Support manual dan via webhook dari payment gateway
- **Calculate Denda**: Otomatis hitung denda Rp 10.000/hari (max Rp 500.000)
- **Block KRS**: Mahasiswa dengan tunggakan tidak bisa mendaftar KRS

### 3. Dashboard Keuangan (20%)
- **Per Mahasiswa**:
  - Total tagihan
  - Sudah dibayar
  - Sisa pembayaran
  - Riwayat transaksi
  
- **Per Program Studi**:
  - Collection rate (%)
  - Total revenue
  - Jumlah siswa aktif
  
- **Grafik & Analytics**:
  - Pembayaran per bulan
  - Trends tunggakan

### 4. Payment Webhook (15%)
- **Endpoint Webhook**: Terima notifikasi dari payment gateway
- **Update Status**: Otomatis update billing dari unpaid → paid
- **Verification**: HMAC-SHA256 signature verification
- **Receipt Email**: Kirim invoice/receipt via email

### 5. AI Financial Report (5%)
- **Analisis Data Pembayaran**: Menganalisis payment patterns
- **Generate Insights**:
  - Total revenue bulan ini
  - Collection rate
  - Top 10 mahasiswa dengan tunggakan terbesar
  - Rekomendasi aksi (reminder, follow-up, dll)
- **Export JSON**: Untuk integrasi dashboard frontend

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- SQLite3
- pip

### Installation

```bash
# Clone repository
cd c:\Users\erwin\Downloads\MODUL_SPP

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Server akan berjalan di: http://localhost:5000

### Database Initialization

Database akan otomatis dibuat saat aplikasi pertama kali dijalankan dengan sample data:
- 4 Program Studi (Teknik Informatika: Rp 5jt, Ekonomi: Rp 4jt, dll)
- 4 Payment Methods (BCA Transfer, Virtual Account, GCash, Credit Card)

## 📚 API Endpoints

### Billing APIs

#### Generate Billing
```http
POST /api/billing/generate/<semester_id>
Content-Type: application/json

{
    "due_days": 14
}

Response:
{
    "success": true,
    "message": "Berhasil generate billing untuk 150 mahasiswa",
    "created_count": 150,
    "failed_count": 0
}
```

#### Get Student Billing
```http
GET /api/billing/student/<student_id>

Response:
{
    "student": {
        "id": 1,
        "nim": "2021000001",
        "name": "Andi Wijaya",
        "program_studi": "Teknik Informatika"
    },
    "summary": {
        "total_billed": 10000000,
        "total_paid": 5000000,
        "total_outstanding": 5000000,
        "payment_percentage": 50.0
    },
    "billings": [...]
}
```

#### Check KRS Eligibility
```http
GET /api/billing/can-register/<student_id>

Response:
{
    "can_register": true,
    "message": "Mahasiswa bisa mendaftar KRS",
    "outstanding": 0
}

// atau jika ada tunggakan:
{
    "can_register": false,
    "message": "Mahasiswa memiliki tunggakan sebesar Rp 5.000.000",
    "outstanding": 5000000
}
```

#### Get Outstanding Billings
```http
GET /api/billing/outstanding?limit=20&offset=0&status=overdue

Response:
{
    "total": 45,
    "limit": 20,
    "offset": 0,
    "billings": [
        {
            "id": 10,
            "student": {
                "nim": "2021000001",
                "name": "Andi Wijaya"
            },
            "semester": "2023/2024-Ganjil",
            "total_amount": 5000000,
            "remaining_amount": 5000000,
            "penalty": 50000,
            "status": "overdue",
            "due_date": "2024-01-29T00:00:00",
            "days_overdue": 5
        }
    ]
}
```

### Payment APIs

#### Process Payment
```http
POST /api/payment/process
Content-Type: application/json

{
    "billing_id": 10,
    "amount": 5000000,
    "payment_method_id": 1,
    "transaction_id": "TXN20240115001",
    "gateway_name": "manual"
}

Response:
{
    "success": true,
    "message": "Pembayaran sebesar Rp 5.000.000 berhasil dicatat",
    "payment": {
        "id": 25,
        "reference_code": "PAY20240115123456ABC",
        "amount": 5000000,
        "status": "confirmed"
    },
    "billing": {
        "id": 10,
        "status": "paid",
        "remaining_amount": 0
    }
}
```

#### Get Payment History
```http
GET /api/payment/history/<student_id>?limit=10

Response:
{
    "total": 3,
    "payments": [
        {
            "id": 25,
            "reference_code": "PAY20240115123456ABC",
            "amount": 5000000,
            "status": "confirmed",
            "payment_date": "2024-01-15T10:30:00",
            "confirmation_date": "2024-01-15T10:30:00",
            "payment_method": "BCA Transfer",
            "gateway": "manual"
        }
    ]
}
```

#### Get Payment Statistics
```http
GET /api/payment/statistics?days=30

Response:
{
    "period": {
        "start_date": "2023-12-16T10:30:00",
        "end_date": "2024-01-15T10:30:00",
        "days": 30
    },
    "statistics": {
        "total_payments": 150,
        "total_amount": 750000000,
        "average_amount": 5000000,
        "daily_average": 25000000
    }
}
```

### Webhook APIs

#### Payment Webhook
```http
POST /api/webhook/payment
Content-Type: application/json

{
    "transaction_id": "TXN20240115001",
    "reference_code": "PAY20240115123456ABC",
    "amount": 5000000,
    "status": "success",
    "timestamp": "2024-01-15T10:30:00",
    "signature": "HMAC_SHA256_SIGNATURE"
}

Response:
{
    "success": true,
    "message": "Webhook processed successfully"
}
```

#### Health Check
```http
GET /api/webhook/health

Response:
{
    "status": "healthy",
    "service": "SPP Payment Webhook Handler",
    "timestamp": "2024-01-15T10:30:00"
}
```

### Dashboard APIs

#### Financial Report
```http
GET /api/dashboard/financial-report?days=30

Response:
{
    "period": {
        "start_date": "2023-12-16T10:30:00",
        "end_date": "2024-01-15T10:30:00"
    },
    "revenue_metrics": {
        "total_revenue": 750000000,
        "total_payments": 150,
        "average_payment": 5000000,
        "total_billed": 1500000000,
        "collection_rate": 50.0
    },
    "outstanding": {
        "total_outstanding": 750000000,
        "total_overdue": 100000000,
        "num_overdue_students": 45
    },
    "top_outstanding_billings": [...],
    "ai_insights": {
        "insights": [
            "🟡 Tingkat pengumpulan sedang: 50.0%",
            "⚠️ 45 mahasiswa dengan tunggakan",
            "💰 Total tunggakan: Rp 750.000.000"
        ],
        "recommendations": [
            "Tingkatkan komunikasi dengan mahasiswa",
            "Prioritas: Kirim reminder ke 5 mahasiswa dengan tunggakan terbesar"
        ]
    }
}
```

#### Student Financial Profile
```http
GET /api/dashboard/student-profile/<student_id>

Response:
{
    "student": {
        "nim": "2021000001",
        "name": "Andi Wijaya",
        "email": "andi@student.com",
        "program_studi": "Teknik Informatika"
    },
    "financial_summary": {
        "total_billed": 10000000,
        "total_paid": 5000000,
        "total_outstanding": 5000000,
        "payment_percentage": 50.0
    },
    "overdue_info": {
        "has_overdue": true,
        "num_overdue_billings": 1,
        "total_overdue_amount": 2500000
    },
    "recent_payments": [...],
    "billing_details": [...]
}
```

#### Dashboard Summary
```http
GET /api/dashboard/summary

Response:
{
    "timestamp": "2024-01-15T10:30:00",
    "metrics": {
        "total_active_students": 500,
        "total_billed": 2500000000,
        "total_paid": 1250000000,
        "total_outstanding": 1250000000,
        "collection_rate": 50.0,
        "students_with_overdue": 75
    }
}
```

#### Program Studi Statistics
```http
GET /api/dashboard/program-studi-stats

Response:
{
    "program_studi_statistics": [
        {
            "program_studi": "Teknik Informatika",
            "num_students": 120,
            "total_billed": 600000000,
            "total_paid": 300000000,
            "collection_rate": 50.0
        },
        {
            "program_studi": "Ekonomi",
            "num_students": 100,
            "total_billed": 400000000,
            "total_paid": 250000000,
            "collection_rate": 62.5
        }
    ]
}
```

## 🔧 Konfigurasi

File `app/config.py`:

```python
# Billing Configuration
BILLING_DAYS_BEFORE_DUE = 14  # Due date 2 minggu setelah semester start
OVERDUE_PENALTY_PER_DAY = 10000  # Rp 10.000 per hari
OVERDUE_MAX_PENALTY = 500000  # Max penalty Rp 500.000

# Program Studi dan SPP Amount
PROGRAM_STUDI_SPP = {
    'Teknik Informatika': 5000000,      # Rp 5 juta
    'Ekonomi': 4000000,                 # Rp 4 juta
    'Hukum': 3500000,                   # Rp 3.5 juta
    'Teknik Sipil': 5500000,            # Rp 5.5 juta
}
```

## 🗓️ Scheduler Configuration

Billing otomatis di-generate sesuai jadwal:

```python
# Generate billing: Hari 1 setiap bulan, jam 00:00
# Update penalty: Setiap hari jam 00:00
# Send reminder: Setiap hari jam 09:00
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_billing_service.py

# Run with coverage
python -m pytest tests/ --cov=app
```

## 📊 Database Schema

### Tabel: students
- id (PK)
- nim (UNIQUE)
- name
- email
- program_studi_id (FK)
- status (active/inactive/graduated)
- created_at, updated_at

### Tabel: billings
- id (PK)
- student_id (FK)
- semester
- total_amount
- paid_amount
- remaining_amount
- penalty
- status (unpaid/partial/paid/overdue)
- due_date
- created_at, updated_at

### Tabel: payments
- id (PK)
- student_id (FK)
- billing_id (FK)
- payment_method_id (FK)
- transaction_id (UNIQUE)
- reference_code (UNIQUE)
- amount
- status (pending/confirmed/failed)
- gateway_response (JSON)
- created_at, updated_at

### Tabel: payment_methods
- id (PK)
- name
- method_type
- provider
- gateway_code
- is_active

## 🔐 Security

1. **Webhook Signature Verification**: HMAC-SHA256
2. **Environment Variables**: Untuk sensitive data
3. **Database Transactions**: Untuk atomicity
4. **Input Validation**: Sanitasi semua input
5. **Error Handling**: Proper error handling tanpa expose sensitive info

## 📝 Kriteria Sukses

- ✅ Billing ter-generate otomatis tiap semester
- ✅ Webhook payment berfungsi (test dengan curl)
- ✅ Dashboard menampilkan data real-time
- ✅ Mahasiswa dengan tunggakan tidak bisa isi KRS
- ✅ Denda keterlambatan ter-update otomatis
- ✅ AI insights ter-generate dengan akurat
- ✅ Email reminder terkirim (optional)

## 📌 Notes

- Database menggunakan SQLite untuk development
- Untuk production, gunakan PostgreSQL atau MySQL
- Environment variables harus di-setup untuk production
- Logging otomatis ke file `logs/` directory
- Payment gateway integration dapat dikustomisasi

## 👨‍💻 Author

SPP Management System v1.0
MINGGU 11: Modul Keuangan (SPP)
Tahun Akademik 2023/2024

## 📄 License

MIT License
