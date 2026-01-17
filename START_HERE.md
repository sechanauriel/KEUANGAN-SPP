# 🎓 SPP Management System

**Sistem Manajemen Keuangan SPP dengan AI Financial Reporting**

---

## ⚡ CARA RUN PALING MUDAH - PILIH SALAH SATU:

### **Cara 1: Klik File (Termudah)** 🖱️
Double-click salah satu file ini:
- **`RUN.bat`** (untuk Windows Command Prompt)
- **`RUN.ps1`** (untuk PowerShell)

Server akan start otomatis!

### **Cara 2: Command Line**
Buka PowerShell dan jalankan:
```powershell
cd C:\Users\erwin\Downloads\MODUL_SPP
.\.venv\Scripts\python.exe app.py
```

### **Cara 3: PowerShell Script**
```powershell
cd C:\Users\erwin\Downloads\MODUL_SPP
.\RUN.ps1
```

---

## 🌐 Akses Web Dashboard

Setelah server jalan, buka browser:

```
http://localhost:5000
```

Atau klik link: [http://localhost:5000](http://localhost:5000)

---

## 📖 DOKUMENTASI

Pilih panduan sesuai kebutuhan:

| File | Deskripsi | Waktu |
|------|-----------|-------|
| **RUN_GUIDE.md** | Panduan super mudah 3-langkah | 5 min |
| **VISUAL_GUIDE.md** | Panduan dengan visual/ASCII | 10 min |
| **QUICK_START.md** | Panduan lengkap + troubleshooting | 20 min |
| **README.md** | API documentation lengkap | 30 min |
| **IMPLEMENTATION_GUIDE.md** | Panduan customize/implementasi | 45 min |
| **PROJECT_SUMMARY.md** | Ringkasan project overview | 15 min |
| **INDEX.md** | Daftar semua dokumentasi | 5 min |

**👉 MULAI DARI: [RUN_GUIDE.md](RUN_GUIDE.md) atau [VISUAL_GUIDE.md](VISUAL_GUIDE.md)**

---

## 📊 QUICK STATS

- ✅ **30+ Python Files** - Production ready code
- ✅ **17 API Endpoints** - Semua business logic
- ✅ **7 Database Tables** - Complete schema
- ✅ **3 Auto Jobs** - APScheduler cron jobs
- ✅ **Web Dashboard** - Interactive API testing
- ✅ **100% Module Complete** - Sesuai module requirements

---

## 🧪 TESTING API

### **Di Web Dashboard** (Termudah)
1. Buka http://localhost:5000
2. Klik "Test API" pada endpoint yang ingin di-test
3. Lihat response JSON

### **Dengan CURL**
Buka PowerShell baru dan jalankan:
```powershell
curl http://localhost:5000/api/dashboard/summary
curl http://localhost:5000/api/billing/outstanding
curl http://localhost:5000/api/dashboard/financial-report?days=30
```

---

## 🎯 MAIN FEATURES

✅ **Billing Management** - Generate tagihan, track status  
✅ **Payment Processing** - Catat pembayaran, webhook handling  
✅ **Penalty Calculation** - Denda otomatis, max cap enforcement  
✅ **Financial Dashboard** - Real-time analytics & reporting  
✅ **AI Insights** - Smart recommendations & analysis  
✅ **KRS Blocking** - Block registration jika ada tunggakan  
✅ **Automatic Scheduler** - 3 cron jobs running 24/7  
✅ **Web Interface** - Beautiful dashboard + API testing  

---

## 🚀 QUICK COMMANDS

```powershell
# Run program
.\.venv\Scripts\python.exe app.py

# Open browser
start http://localhost:5000

# Test API
curl http://localhost:5000/api/dashboard/summary

# Stop server
CTRL + C
```

---

## ❌ ERROR? QUICK FIX

| Error | Solusi |
|-------|--------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Address already in use | `taskkill /F /IM python.exe` |
| Template not found | Pastikan `app/templates/index.html` ada |
| Port 5000 busy | Ubah port di `app/config.py` |

Lihat **QUICK_START.md** untuk troubleshooting lengkap.

---

## 📚 PROJECT STRUCTURE

```
MODUL_SPP/
├── RUN.bat / RUN.ps1 ← KLIK UNTUK RUN
├── app.py ← Main file
├── requirements.txt ← Dependencies
├── 📖 Dokumentasi
│   ├── RUN_GUIDE.md ⭐
│   ├── VISUAL_GUIDE.md ⭐
│   ├── QUICK_START.md
│   ├── README.md
│   └── ... (6 files dokumentasi)
├── app/ ← Aplikasi
│   ├── models/ ← Database models
│   ├── services/ ← Business logic
│   ├── routes/ ← API endpoints
│   ├── schedulers/ ← Cron jobs
│   ├── templates/ ← Web interface
│   └── utils/ ← Helpers
└── tests/ ← Unit tests
```

---

## 💡 TIPS

- **Double-click RUN.bat** untuk start termudah
- **Jangan tutup PowerShell** yang jalankan server
- **Refresh browser** (Ctrl+F5) jika ada perubahan
- **Baca RUN_GUIDE.md** untuk panduan step-by-step

---

## ✨ SELESAI!

Sekarang Anda siap untuk:
✅ Run program  
✅ Test API  
✅ Explore features  
✅ Customize code  

---

## 📞 BANTUAN

- **Panduan**: Baca file dokumentasi (lihat tabel di atas)
- **Error**: Lihat troubleshooting di QUICK_START.md
- **API Detail**: Lihat README.md
- **Code Customize**: Lihat IMPLEMENTATION_GUIDE.md

---

**Selamat menggunakan SPP Management System!** 🎉

**[👉 START DARI SINI: RUN_GUIDE.md](RUN_GUIDE.md)**
