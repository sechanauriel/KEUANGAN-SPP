# 📸 VISUAL STEP-BY-STEP GUIDE

## STEP 1: Open PowerShell

Tekan **Windows Key** dan ketik "PowerShell":

```
Windows Key
    ↓
Ketik: PowerShell
    ↓
Klik: Windows PowerShell
    ↓
PowerShell terbuka
```

---

## STEP 2: Navigate to Folder

Copy-paste ini di PowerShell dan tekan ENTER:

```
cd C:\Users\erwin\Downloads\MODUL_SPP
```

**Output yang benar:**
```
PS C:\Users\erwin\Downloads\MODUL_SPP>
```

---

## STEP 3: Run the Program

Copy-paste ini di PowerShell dan tekan ENTER:

```
.\.venv\Scripts\python.exe app.py
```

**Tunggu sampai output muncul:**

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
   Press CTRL+C to stop

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.7:5000
```

**✅ BERHASIL! Server sudah jalan!**

---

## STEP 4: Open Web Browser

Buka **browser favorit** (Chrome, Firefox, Edge, Safari, etc):

**Ketik di address bar:**
```
http://localhost:5000
```

Atau **copy-paste link ini:**
```
http://localhost:5000
```

---

## STEP 5: Web Dashboard Muncul

Halaman web akan muncul dengan tampilan:

```
╔════════════════════════════════════════════════╗
║  🎓 SPP Management System                      ║
║  API Dashboard - MINGGU 11: Modul Keuangan    ║
╚════════════════════════════════════════════════╝

┌─────────────────┬──────────────┬────────────┬─────────────┐
│ Total Mahasiswa │ Total Tagihan│ Total Bayar│ Collection  │
│       -         │      -       │     -      │     -       │
└─────────────────┴──────────────┴────────────┴─────────────┘

📋 BILLING APIs
┌─────────────────────────────────────────┐
│ GET Lihat Tagihan Mahasiswa             │
│ [Test API] [Copy]                       │
├─────────────────────────────────────────┤
│ GET Cek Boleh Isi KRS                   │
│ [Test API] [Copy]                       │
├─────────────────────────────────────────┤
│ GET Daftar Tagihan Outstanding          │
│ [Test API] [Copy]                       │
└─────────────────────────────────────────┘

💳 PAYMENT APIs
[...]

📊 DASHBOARD APIs
[...]

🔗 WEBHOOK APIs
[...]
```

---

## STEP 6: Test API

### Cara 1: Di Web (Paling Mudah)

1. **Scroll** halaman web ke bawah
2. **Cari API** yang ingin di-test (mis: "Dashboard Summary")
3. **Klik tombol** "Test API" 
4. **Response** akan muncul di popup

```
┌──────────────────────────────┐
│ API Response                 │
├──────────────────────────────┤
│ {                            │
│   "timestamp": "...",        │
│   "metrics": {               │
│     "total_students": 4,     │
│     "total_billed": 20000000,│
│     "total_paid": 0,         │
│     "collection_rate": 0.0   │
│   }                          │
│ }                            │
└──────────────────────────────┘
```

### Cara 2: Dengan CURL Command

**Buka PowerShell BARU** (jangan tutup yang jalankan server):

```powershell
cd C:\Users\erwin\Downloads\MODUL_SPP
```

Tekan ENTER, kemudian:

```powershell
curl http://localhost:5000/api/dashboard/summary
```

Tekan ENTER, response akan keluar sebagai JSON.

---

## SUMMARY - Flow Keseluruhan

```
┌─────────────────────────────────────────┐
│ 1. Open PowerShell                      │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 2. cd C:\Users\erwin\Downloads\MODUL_SPP│
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 3. .\.venv\Scripts\python.exe app.py    │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 4. Wait untuk "Server running at..."    │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 5. Open browser http://localhost:5000   │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 6. Web Dashboard Muncul                 │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 7. Click [Test API] untuk testing       │
└────────────┬────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────┐
│ 8. Response JSON Muncul di Popup        │
└─────────────────────────────────────────┘
```

---

## STOP/RESTART Program

### Untuk STOP:
Di PowerShell yang jalankan program, tekan:
```
CTRL + C
```

**Output:**
```
^C
KeyboardInterrupt
PS C:\Users\erwin\Downloads\MODUL_SPP>
```

### Untuk RESTART:
Jalankan lagi command yang sama:
```powershell
.\.venv\Scripts\python.exe app.py
```

---

## API EXAMPLES

### Example 1: Get Dashboard Summary
```powershell
curl http://localhost:5000/api/dashboard/summary
```

**Response:**
```json
{
  "timestamp": "2024-09-14T10:30:00.123456",
  "metrics": {
    "total_active_students": 4,
    "total_billed": 20000000,
    "total_paid": 0,
    "total_outstanding": 20000000,
    "collection_rate": 0.0,
    "students_with_overdue": 0
  }
}
```

### Example 2: Get Outstanding Billings
```powershell
curl http://localhost:5000/api/billing/outstanding
```

**Response:**
```json
{
  "outstanding_count": 4,
  "total_outstanding": 20000000,
  "billings": [
    {
      "id": 1,
      "student_name": "John Doe",
      "semester": "2024/2025-Ganjil",
      "total_amount": 5000000,
      "remaining_amount": 5000000,
      "status": "unpaid",
      "due_date": "2024-09-14"
    },
    ...
  ]
}
```

### Example 3: Get Financial Report
```powershell
curl http://localhost:5000/api/dashboard/financial-report?days=30
```

**Response:**
```json
{
  "period": "Last 30 days",
  "report_date": "2024-09-14",
  "metrics": {
    "total_revenue": 0,
    "total_payments": 0,
    "num_students_paid": 0,
    "collection_rate": 0.0
  },
  "ai_insights": {
    "overall_status": "🟡 Monitor situation",
    "revenue_trend": "📉 No revenue yet",
    "collection_analysis": "🔴 No payments received"
  },
  "recommendations": [
    "Send payment reminders to all students",
    "Follow up with 30+ days overdue",
    "Consider payment arrangement options"
  ]
}
```

---

## TROUBLESHOOTING QUICK FIX

### Error: "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install -r requirements.txt
```

### Error: "Address already in use"
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Error: "Template not found"
Pastikan file ada:
```
app/templates/index.html
```

### Browser tidak bisa akses
1. Pastikan server masih jalan (cek PowerShell)
2. Refresh browser: Ctrl + F5
3. Coba URL lain: `http://127.0.0.1:5000`

---

## ✅ SUCCESS CHECKLIST

- [ ] PowerShell sudah terbuka
- [ ] Folder MODUL_SPP sudah di-navigate
- [ ] Program sudah di-run dengan `.\.venv\Scripts\python.exe app.py`
- [ ] Output "Server running at: http://localhost:5000" muncul
- [ ] Browser sudah buka `http://localhost:5000`
- [ ] Web dashboard sudah muncul
- [ ] Bisa klik "Test API" dan melihat response

**Jika semua ✅, SELAMAT! Program sudah berhasil dijalankan!** 🎉

---

**Masih ada pertanyaan? Baca file dokumentasi lain (README.md, IMPLEMENTATION_GUIDE.md, PROJECT_SUMMARY.md)**

**Happy Testing! 🚀**
