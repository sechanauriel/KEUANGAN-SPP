# 📖 CARA RUN PROGRAM - SIMPLE GUIDE

## 🎯 3 STEP SAJA!

### **STEP 1️⃣ : Buka PowerShell/Terminal**

```
Windows Key → ketik "PowerShell" → Enter
```

### **STEP 2️⃣ : Masuk Folder Project**

Salin & paste command ini di PowerShell:

```powershell
cd C:\Users\erwin\Downloads\MODUL_SPP
```

Tekan **ENTER**

### **STEP 3️⃣ : Jalankan Program**

Salin & paste command ini:

```powershell
.\.venv\Scripts\python.exe app.py
```

Tekan **ENTER** dan **TUNGGU** sampai keluar output:

```
✅ Database initialized at: spp_management.db
▶️  Starting Flask development server...
   Server running at: http://localhost:5000
```

---

## ✨ SELESAI! Program Sudah Jalan

Sekarang buka **Browser** dan ketik:

```
http://localhost:5000
```

Atau klik link: [http://localhost:5000](http://localhost:5000)

---

## 📊 Apa yang Akan Muncul?

Halaman web dengan:
- 📈 Dashboard statistics (mahasiswa, tagihan, pembayaran)
- 🧪 Tombol untuk test semua API
- 📋 Lihat list semua endpoints
- 📝 Copy endpoint URL untuk curl testing

---

## 🧪 Testing API di Browser

### Di halaman web (http://localhost:5000):

1. Scroll ke bawah cari API yang mau di-test
2. Klik tombol **"Test API"**
3. Lihat hasilnya di popup

**Contoh API yang bisa di-test:**
- `GET /api/dashboard/summary` → Lihat statistik
- `GET /api/billing/outstanding` → Lihat tagihan outstanding
- `GET /api/dashboard/financial-report` → Laporan keuangan
- `GET /api/payment/statistics` → Statistik pembayaran

---

## 💻 Testing API dengan Command Line

Buka **PowerShell BARU** (jangan tutup PowerShell yang jalankan server):

```powershell
# Test 1: Dashboard Summary
curl http://localhost:5000/api/dashboard/summary

# Test 2: Outstanding Billings
curl http://localhost:5000/api/billing/outstanding

# Test 3: Financial Report
curl http://localhost:5000/api/dashboard/financial-report?days=30

# Test 4: Payment Statistics
curl http://localhost:5000/api/payment/statistics

# Test 5: Health Check
curl http://localhost:5000/api/webhook/health
```

Hasil akan keluar sebagai **JSON** di terminal.

---

## 🛑 Cara Menghentikan Program

Di PowerShell yang jalankan program, tekan:

```
CTRL + C
```

Program akan berhenti.

---

## ❌ Jika Ada Error

### **Error: ModuleNotFoundError**

```powershell
pip install -r requirements.txt
```

### **Error: Address already in use**

Port 5000 sedang dipakai. Cari process yang pakai port:

```powershell
netstat -ano | findstr :5000
```

Lihat PID-nya, lalu:

```powershell
taskkill /PID <ganti-dengan-PID> /F
```

### **Browser tidak bisa akses localhost:5000**

1. Pastikan server masih jalan (lihat PowerShell)
2. Refresh browser (Ctrl + F5)
3. Coba URL lain:
   - `http://127.0.0.1:5000`
   - `http://192.168.1.7:5000`

---

## 📂 File yang Penting

```
MODUL_SPP/
├── app.py                      ← File utama untuk run
├── requirements.txt            ← Dependencies
├── spp_management.db          ← Database (auto-created)
├── QUICK_START.md             ← Panduan ini
├── README.md                  ← Dokumentasi lengkap
├── IMPLEMENTATION_GUIDE.md    ← Panduan implementasi
├── PROJECT_SUMMARY.md         ← Ringkasan project
└── app/
    ├── templates/index.html   ← Web dashboard
    ├── models/                ← Database models
    ├── services/              ← Business logic
    ├── routes/                ← API endpoints
    ├── schedulers/            ← Cron jobs
    └── utils/                 ← Helper functions
```

---

## 🚀 COMMANDS REFERENCE

### Install dependencies (hanya 1x)
```powershell
pip install -r requirements.txt
```

### Run program
```powershell
.\.venv\Scripts\python.exe app.py
```

### Buka web dashboard
```
Browser: http://localhost:5000
```

### Test API dengan curl
```powershell
curl http://localhost:5000/api/dashboard/summary
```

### Stop program
```
Tekan CTRL + C di PowerShell
```

### Reset database
```powershell
rm spp_management.db
```

---

## ✅ CHECKLIST - Pastikan Semua Sudah Benar

- [ ] PowerShell sudah terbuka
- [ ] Sudah `cd` ke folder MODUL_SPP
- [ ] Jalankan `.\.venv\Scripts\python.exe app.py`
- [ ] Tunggu sampai muncul `Server running at: http://localhost:5000`
- [ ] Buka browser ke `http://localhost:5000`
- [ ] Halaman web dashboard muncul
- [ ] Click tombol "Test API" untuk testing
- [ ] Lihat response JSON muncul

**Jika semua checklist sudah ✅, maka program sudah berhasil dijalankan!**

---

## 💡 TIPS

- **Jangan tutup PowerShell** yang menjalankan server
- Buka **PowerShell baru** untuk command curl testing
- **Refresh browser** (Ctrl + F5) jika ada perubahan
- Baca **README.md** untuk API documentation lengkap

---

**SELAMAT! Anda sudah bisa menjalankan SPP Management System!** 🎉

Butuh bantuan? Baca file dokumentasi lain atau troubleshooting di atas.
