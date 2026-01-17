# 🚀 QUICK START GUIDE - SPP Management System

## 📋 Daftar Isi
1. [Prasyarat](#prasyarat)
2. [Instalasi](#instalasi)
3. [Cara Menjalankan](#cara-menjalankan)
4. [Akses Web Dashboard](#akses-web-dashboard)
5. [Testing API](#testing-api)
6. [Troubleshooting](#troubleshooting)

---

## ✅ Prasyarat

Sebelum menjalankan program, pastikan sudah tersedia:
- **Python 3.8+** (sudah terinstall)
- **Folder project**: `C:\Users\erwin\Downloads\MODUL_SPP\`
- **Virtual Environment**: `.venv` (sudah ada di folder)

Cek versi Python:
```powershell
python --version
```

---

## 📦 Instalasi (Jika Pertama Kali)

### Step 1: Buka Terminal/PowerShell

```powershell
cd C:\Users\erwin\Downloads\MODUL_SPP
```

### Step 2: Aktifkan Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

Jika error permission, jalankan command ini dulu:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

Output berhasil akan menunjukkan:
```
Successfully installed Flask-2.3.3 Flask-SQLAlchemy-3.0.5 APScheduler-3.10.4 ...
```

---

## 🏃 Cara Menjalankan

### **CARA PALING MUDAH** 👇

Buka PowerShell dan jalankan:

```powershell
cd C:\Users\erwin\Downloads\MODUL_SPP
.\.venv\Scripts\python.exe app.py
```

**Tunggu sampai muncul output seperti ini:**

```
╔════════════════════════════════════════════════════════════════════════╗
║   SPP MANAGEMENT SYSTEM - MINGGU 11: Modul Keuangan                   ║
║   Payment Management with AI Financial Reporting                       ║
╚════════════════════════════════════════════════════════════════════════╝

✅ Database initialized at: spp_management.db
📚 API Documentation:
   - Billing APIs: http://localhost:5000/api/billing
   - Payment APIs: http://localhost:5000/api/payment
   - Webhook APIs: http://localhost:5000/api/webhook
   - Dashboard APIs: http://localhost:5000/api/dashboard

▶️  Starting Flask development server...
   Server running at: http://localhost:5000
```

**Selesai!** Server sudah berjalan 🎉

---

## 🌐 Akses Web Dashboard

### **Cara 1: Buka Browser**

Buka browser favorit Anda dan pergi ke:

```
http://localhost:5000
```

Atau:

```
http://127.0.0.1:5000
```

### **Tampilannya:**

- ✨ Dashboard cantik dengan interface user-friendly
- 📊 Real-time statistics (total mahasiswa, tagihan, pembayaran)
- 🧪 Test semua API langsung di browser
- 📋 Lihat response JSON dengan format rapi
- 📋 Lihat semua API endpoints yang tersedia

---

## 🧪 Testing API

### **Dari Web Dashboard** (Paling Mudah)

1. Buka http://localhost:5000
2. Cari API yang ingin di-test
3. Klik tombol **"Test API"** 
4. Lihat response di popup

### **Dari Terminal dengan CURL**

Buka PowerShell **BARU** (jangan close yang jalankan server):

```powershell
# Test 1: Dashboard Summary
curl http://localhost:5000/api/dashboard/summary

# Test 2: Financial Report
curl http://localhost:5000/api/dashboard/financial-report?days=30

# Test 3: Program Studi Statistics
curl http://localhost:5000/api/dashboard/program-studi-stats

# Test 4: Billing Outstanding
curl http://localhost:5000/api/billing/outstanding

# Test 5: Payment Statistics
curl http://localhost:5000/api/payment/statistics

# Test 6: Health Check
curl http://localhost:5000/api/webhook/health
```

---

## 📊 Contoh API Testing Lengkap

### **Test 1: Lihat Tagihan Mahasiswa**

```powershell
curl http://localhost:5000/api/billing/student/1
```

**Response:**
```json
{
  "student": {
    "id": 1,
    "nim": "STU001",
    "name": "John Doe"
  },
  "billings": [
    {
      "id": 1,
      "semester": "2024/2025-Ganjil",
      "total_amount": 5000000,
      "paid_amount": 0,
      "remaining_amount": 5000000,
      "penalty": 0,
      "status": "unpaid",
      "due_date": "2024-09-14"
    }
  ]
}
```

### **Test 2: Proses Pembayaran Manual**

```powershell
$body = @{
    billing_id = 1
    amount = 5000000
    payment_method_id = 1
    transaction_id = "TXN-" + [datetime]::Now.Ticks
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:5000/api/payment/process" `
    -Method POST `
    -Headers @{'Content-Type' = 'application/json'} `
    -Body $body
```

### **Test 3: Cek Boleh Isi KRS**

```powershell
curl http://localhost:5000/api/billing/can-register/1
```

**Response:**
```json
{
  "student_id": 1,
  "can_register": true,
  "outstanding": 0,
  "message": "Student can register for KRS"
}
```

### **Test 4: Laporan Keuangan dengan AI**

```powershell
curl http://localhost:5000/api/dashboard/financial-report?days=30
```

**Response:**
```json
{
  "period": "Last 30 days",
  "report_date": "2024-09-14",
  "metrics": {
    "total_revenue": 20000000,
    "total_payments": 20000000,
    "num_students_paid": 4,
    "collection_rate": 100.0
  },
  "ai_insights": {
    "overall_status": "✅ Excellent Performance",
    "revenue_trend": "📈 Upward trend",
    "collection_analysis": "🟢 All students have paid"
  },
  "recommendations": [
    "Monitor new students",
    "Send reminder to pending payments"
  ]
}
```

---

## 🎯 Semua API Endpoints

### **BILLING** 📋
```
GET  /api/billing/student/<student_id>
GET  /api/billing/can-register/<student_id>
GET  /api/billing/outstanding
POST /api/billing/generate/<semester_id>
POST /api/billing/update-penalty/<billing_id>
```

### **PAYMENT** 💳
```
GET  /api/payment/history/<student_id>
GET  /api/payment/statistics
GET  /api/payment/<payment_id>
POST /api/payment/process
```

### **DASHBOARD** 📊
```
GET /api/dashboard/summary
GET /api/dashboard/financial-report?days=30
GET /api/dashboard/program-studi-stats
GET /api/dashboard/student-profile/<student_id>
```

### **WEBHOOK** 🔗
```
GET /api/webhook/health
POST /api/webhook/payment
POST /api/webhook/test
```

---

## 🛑 Menghentikan Server

Tekan **CTRL + C** di terminal yang menjalankan server:

```
Press CTRL+C to quit
^C
```

Server akan berhenti dan terminal siap untuk command berikutnya.

---

## 🔧 Troubleshooting

### **Error: ModuleNotFoundError: No module named 'flask'**

**Solusi:** Install dependencies
```powershell
pip install -r requirements.txt
```

### **Error: Address already in use (port 5000)**

**Solusi:** Ada proses lain yang menggunakan port 5000. Jalankan:

```powershell
# Cari process yang pakai port 5000
netstat -ano | findstr :5000

# Kill process (ganti PID dengan number dari output di atas)
taskkill /PID <PID> /F

# Contoh:
taskkill /PID 12345 /F
```

### **Error: Database locked**

**Solusi:** Hapus file database dan restart:

```powershell
rm spp_management.db
.\.venv\Scripts\python.exe app.py
```

### **Browser tidak bisa akses localhost:5000**

**Solusi:**

1. Pastikan server masih berjalan (lihat output di PowerShell)
2. Coba akses dengan URL berbeda:
   - `http://127.0.0.1:5000`
   - `http://localhost:5000`
   - `http://192.168.1.7:5000` (IP local Anda)
3. Refresh browser (Ctrl + F5)

### **Template not found error**

**Solusi:** Pastikan folder `app/templates/` ada dan berisi `index.html`:

```powershell
ls app/templates/
```

Harus ada output:
```
    Directory: C:\Users\erwin\Downloads\MODUL_SPP\app\templates

Mode                 LastWriteTime         Length Name
----                 -----------         ------ ----
-a---           1/17/2026 11:00 AM      123456 index.html
```

---

## 💡 Tips & Tricks

### **Jalankan di Background (Windows)**

```powershell
# Buat file run.ps1 dengan isi:
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\erwin\Downloads\MODUL_SPP; .\.venv\Scripts\python.exe app.py"
```

### **Lihat Log File**

```powershell
# Lihat log terbaru
tail -f logs/app.log
```

### **Reset Database**

```powershell
# Hapus database
rm spp_management.db

# Restart server
.\.venv\Scripts\python.exe app.py
```

---

## 📚 Dokumentasi Lengkap

Untuk detail lebih lanjut, baca file dokumentasi:

```powershell
# Dokumentasi API
cat README.md

# Panduan Implementasi
cat IMPLEMENTATION_GUIDE.md

# Ringkasan Project
cat PROJECT_SUMMARY.md
```

---

## ✨ Selesai!

Sekarang Anda sudah siap:

✅ Menjalankan sistem SPP Management  
✅ Akses API melalui web dashboard  
✅ Test semua endpoints  
✅ Lihat hasil response JSON  

**Senang menggunakan SPP Management System!** 🎉

---

**Butuh bantuan?** Baca troubleshooting section di atas atau buka documentasi lengkap.

**Happy Testing!** 🚀
