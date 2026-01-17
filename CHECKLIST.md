# 📝 CHECKLIST - Tahap Demi Tahap

Gunakan checklist ini untuk memastikan semua langkah terselesaikan dengan benar.

---

## ✅ SETUP (Lakukan 1x saja)

- [ ] Buka folder `C:\Users\erwin\Downloads\MODUL_SPP` di File Explorer
- [ ] Pastikan folder `app` ada di dalam
- [ ] Pastikan file `app.py` ada di dalam
- [ ] Pastikan file `requirements.txt` ada di dalam

---

## ✅ INSTALL DEPENDENCIES

- [ ] Buka PowerShell
- [ ] Copy-paste: `cd C:\Users\erwin\Downloads\MODUL_SPP`
- [ ] Tekan ENTER
- [ ] Cek apakah folder sudah di-navigate (lihat di prompt)
- [ ] Copy-paste: `pip install -r requirements.txt`
- [ ] Tekan ENTER
- [ ] Tunggu sampai selesai (lihat "Successfully installed")

---

## ✅ RUN PROGRAM

### Cara 1: Klik File (Termudah)
- [ ] Di File Explorer, double-click `RUN.bat` atau `RUN.ps1`
- [ ] PowerShell/Command Prompt akan terbuka
- [ ] Tunggu sampai keluar "Server running at: http://localhost:5000"
- [ ] Jangan tutup window ini!

### Cara 2: Manual Command
- [ ] Buka PowerShell baru
- [ ] Copy-paste: `cd C:\Users\erwin\Downloads\MODUL_SPP`
- [ ] Tekan ENTER
- [ ] Copy-paste: `.\.venv\Scripts\python.exe app.py`
- [ ] Tekan ENTER
- [ ] Tunggu sampai keluar "Server running at: http://localhost:5000"
- [ ] Jangan tutup window ini!

---

## ✅ AKSES WEB DASHBOARD

- [ ] Buka browser (Chrome, Firefox, Edge, Safari, dll)
- [ ] Di address bar, ketik: `http://localhost:5000`
- [ ] Tekan ENTER
- [ ] Tunggu halaman muncul
- [ ] Lihat header "🎓 SPP Management System"
- [ ] Lihat 4 kotak statistik (Total Mahasiswa, Total Tagihan, dll)
- [ ] Scroll ke bawah lihat API cards

---

## ✅ TEST API DI WEB

- [ ] Cari API yang ingin di-test (mis: "Dashboard Summary")
- [ ] Klik tombol berwarna biru "Test API"
- [ ] Tunggu popup muncul dengan loading spinner
- [ ] Lihat response JSON di popup
- [ ] Tutup popup (klik X atau area kosong)
- [ ] Test API lain untuk verifikasi

---

## ✅ TEST API DENGAN CURL (Optional)

- [ ] Buka PowerShell BARU (jangan tutup yang jalankan server)
- [ ] Copy-paste: `curl http://localhost:5000/api/dashboard/summary`
- [ ] Tekan ENTER
- [ ] Lihat output JSON di terminal
- [ ] Test API lain jika ingin

---

## ✅ STOP PROGRAM

- [ ] Di PowerShell yang menjalankan server, tekan: `CTRL + C`
- [ ] Lihat prompt kembali ke PowerShell
- [ ] Window PowerShell tetap bisa tutup atau tinggalkan terbuka

---

## 🎯 SUCCESS INDICATORS

Jika semua ini ✅, berarti program berhasil:

- [ ] PowerShell menampilkan "Server running at: http://localhost:5000"
- [ ] Browser bisa akses http://localhost:5000
- [ ] Halaman web dashboard muncul dengan data
- [ ] Klik tombol "Test API" dan lihat response JSON
- [ ] Tidak ada error message di PowerShell

---

## ❌ JIKA ADA ERROR

### Error: "ModuleNotFoundError: No module named 'flask'"
- [ ] Jalankan: `pip install -r requirements.txt`
- [ ] Tunggu sampai selesai
- [ ] Jalankan program lagi

### Error: "Address already in use"
- [ ] Ada program lain yang pakai port 5000
- [ ] Jalankan: `taskkill /F /IM python.exe`
- [ ] Jalankan program lagi

### Error: "Template not found"
- [ ] Pastikan folder `app/templates/` ada
- [ ] Pastikan file `app/templates/index.html` ada
- [ ] Jalankan program lagi

### Browser tidak bisa akses localhost:5000
- [ ] Pastikan PowerShell yang jalankan server masih terbuka
- [ ] Lihat PowerShell, pastikan tidak ada error
- [ ] Refresh browser: Ctrl + F5
- [ ] Coba URL lain: `http://127.0.0.1:5000`

---

## 📚 NEXT STEPS SETELAH BERHASIL

- [ ] Baca **RUN_GUIDE.md** untuk detail lebih lanjut
- [ ] Baca **README.md** untuk API documentation
- [ ] Baca **IMPLEMENTATION_GUIDE.md** jika ingin customize
- [ ] Baca **PROJECT_SUMMARY.md** untuk project overview
- [ ] Explore semua API endpoints di web dashboard

---

## 💾 SAVE THIS CHECKLIST

Print atau screenshot checklist ini untuk referensi.

Kapan Anda butuh run program lagi, tinggal ikuti checklist di atas!

---

**Selamat! Anda sudah berhasil menjalankan SPP Management System!** 🎉
