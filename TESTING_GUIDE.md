# 🧪 SPP Management System - Testing & API Guide

## 📋 Fitur yang Diimplementasikan

### ✅ 1. Billing Auto-Generate Per Semester
**Status**: ✅ AKTIF
- Scheduler APScheduler berjalan di background
- Generate billing otomatis: **Hari 1 setiap bulan pukul 00:00**
- Update penalty: **Setiap hari pukul 00:00**
- Send reminder: **Setiap hari pukul 09:00**

#### Manual Trigger (Testing)
```bash
# Trigger billing generation untuk semester aktif
curl -X POST http://localhost:5000/api/billing/generate/1 \
  -H "Content-Type: application/json" \
  -d '{
    "due_days": 14
  }'

# Response:
{
  "success": true,
  "message": "Berhasil generate billing untuk 3 mahasiswa",
  "created_count": 3,
  "failed_count": 0
}
```

#### Check Outstanding Billing
```bash
# Lihat semua billing yang belum lunas
curl -X GET http://localhost:5000/api/billing/outstanding
```

#### Get Student Billing
```bash
# Lihat billing untuk student tertentu
curl -X GET http://localhost:5000/api/billing/student/1
```

---

### ✅ 2. Webhook Payment Functionality
**Status**: ✅ AKTIF
- Endpoint: `POST /api/webhook/payment`
- Signature verification: HMAC-SHA256
- Otomatis update payment status dan billing

#### Test 1: Simple Payment Webhook
```bash
# Webhook payment notification
curl -X POST http://localhost:5000/api/webhook/payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-2026-001",
    "reference_code": "PAY-00001-2026",
    "amount": 1000000,
    "status": "success",
    "timestamp": "2026-01-17T17:30:00",
    "billing_id": 1,
    "student_id": 1,
    "payment_method": "credit_card",
    "signature": ""
  }'

# Response Success:
{
  "success": true,
  "message": "Payment recorded successfully",
  "payment_id": 1,
  "billing_updated": true
}
```

#### Test 2: Test Webhook Endpoint (Development Only)
```bash
# Test endpoint - development only
curl -X POST http://localhost:5000/api/webhook/test \
  -H "Content-Type: application/json" \
  -d '{
    "test_data": "This is a test",
    "timestamp": "2026-01-17T17:30:00"
  }'

# Response:
{
  "success": true,
  "message": "Webhook test successful",
  "received_payload": {
    "test_data": "This is a test",
    "timestamp": "2026-01-17T17:30:00"
  }
}
```

#### Test 3: Webhook Health Check
```bash
# Health check
curl -X GET http://localhost:5000/api/webhook/health

# Response:
{
  "status": "healthy",
  "service": "SPP Payment Webhook Handler",
  "timestamp": "2026-01-17T17:30:00.123456"
}
```

#### Test 4: Multiple Payments for Same Billing (Partial Payment)
```bash
# Payment 1: Partial payment
curl -X POST http://localhost:5000/api/webhook/payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-2026-002",
    "reference_code": "PAY-00002-2026",
    "amount": 2500000,
    "status": "success",
    "timestamp": "2026-01-17T17:35:00",
    "billing_id": 2,
    "student_id": 2,
    "payment_method": "transfer"
  }'

# Payment 2: Second payment (complete)
curl -X POST http://localhost:5000/api/webhook/payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-2026-003",
    "reference_code": "PAY-00003-2026",
    "amount": 2500000,
    "status": "success",
    "timestamp": "2026-01-17T17:40:00",
    "billing_id": 2,
    "student_id": 2,
    "payment_method": "transfer"
  }'

# After 2nd payment, billing status should be PAID
```

---

### ✅ 3. Real-Time Dashboard
**Status**: ✅ AKTIF
- Endpoint: `GET /api/dashboard/summary`
- Update: Real-time dari database
- Metrics: Total students, billed amount, paid amount, outstanding, collection rate

#### Test 1: Dashboard Summary (Real-Time)
```bash
# Get dashboard summary dengan data real-time
curl -X GET http://localhost:5000/api/dashboard/summary

# Response:
{
  "timestamp": "2026-01-17T17:45:00.000000",
  "metrics": {
    "total_active_students": 3,
    "total_billed": 15000000,
    "total_paid": 5000000,
    "total_outstanding": 10000000,
    "collection_rate": 33.33,
    "students_with_overdue": 1
  }
}
```

#### Test 2: Financial Report (Analytics)
```bash
# Get financial report dengan insights
curl -X GET "http://localhost:5000/api/dashboard/financial-report?days=30"

# Response:
{
  "period": {
    "start_date": "2025-12-18",
    "end_date": "2026-01-17",
    "days": 30
  },
  "summary": {
    "total_transactions": 5,
    "total_received": 5000000,
    "average_payment": 1000000
  },
  "insights": [
    "Collection rate is good...",
    "Outstanding billings are...",
    ...
  ],
  "recommendations": [...]
}
```

#### Test 3: Student Financial Profile
```bash
# Get profil keuangan lengkap untuk satu mahasiswa
curl -X GET http://localhost:5000/api/dashboard/student-profile/1

# Response:
{
  "student": {
    "id": 1,
    "nim": "2023001",
    "name": "John Doe",
    "program_studi": "Teknik Informatika"
  },
  "financial_summary": {
    "total_billed": 5000000,
    "total_paid": 1000000,
    "total_outstanding": 4000000,
    "status": "unpaid"
  },
  "billings": [...],
  "payments": [...]
}
```

#### Test 4: Program Studi Statistics
```bash
# Get statistics per program studi
curl -X GET http://localhost:5000/api/dashboard/program-studi-stats

# Response:
{
  "program_studi_statistics": [
    {
      "program_studi": "Teknik Informatika",
      "num_students": 2,
      "total_billed": 10000000,
      "total_paid": 2000000,
      "collection_rate": 20.0
    },
    ...
  ]
}
```

#### Test 5: Billing Breakdown (Real-Time)
```bash
# Get breakdown billing berdasarkan status
curl -X GET http://localhost:5000/api/dashboard/billing-breakdown

# Response:
{
  "timestamp": "2026-01-17T18:20:00.000000",
  "breakdown": {
    "unpaid": {
      "count": 2,
      "total": 10000000
    },
    "partial": {
      "count": 1,
      "total": 5000000
    },
    "paid": {
      "count": 1,
      "total": 5000000
    },
    "overdue": {
      "count": 0,
      "total": 0
    }
  }
}
```

#### Test 6: Students Payment Status Report (Real-Time)
```bash
# Get status pembayaran semua student
curl -X GET http://localhost:5000/api/dashboard/students-status

# Response:
{
  "timestamp": "2026-01-17T18:22:00.000000",
  "filter": "all",
  "pagination": {
    "offset": 0,
    "limit": 100,
    "total": 3
  },
  "students": [
    {
      "student_id": 1,
      "nim": "2023001",
      "name": "John Doe",
      "program_studi": "Teknik Informatika",
      "total_outstanding": 0,
      "latest_billing_status": "paid",
      "can_register_krs": true
    },
    {
      "student_id": 2,
      "nim": "2023002",
      "name": "Jane Smith",
      "program_studi": "Teknik Informatika",
      "total_outstanding": 5000000,
      "latest_billing_status": "unpaid",
      "can_register_krs": false
    },
    ...
  ]
}
```

Filter by status:
```bash
# Hanya lihat student dengan unpaid billing
curl -X GET "http://localhost:5000/api/dashboard/students-status?status=unpaid"

# Hanya lihat student dengan partial payment
curl -X GET "http://localhost:5000/api/dashboard/students-status?status=partial"
```

#### Test 7: Daily Report (Real-Time)
```bash
# Get laporan harian
curl -X GET http://localhost:5000/api/dashboard/daily-report

# Response:
{
  "timestamp": "2026-01-17T18:25:00.000000",
  "report_date": "2026-01-17",
  "summary": {
    "payments_received_today": 7500000,
    "payments_count": 3,
    "new_billings": 0,
    "overdue_count": 1
  },
  "trends": {
    "collection_rate": 40.0,
    "average_payment": 2500000
  }
}
```

---

### ✅ 4. Block KRS for Students with Arrears
**Status**: ✅ AKTIF
- Endpoint: `GET /api/billing/can-register/<student_id>`
- Return: 403 Forbidden jika ada tunggakan
- Check eligibility: `GET /api/billing/krs-eligibility-report`

#### Test 1: Student CAN Register KRS (No Arrears)
```bash
# Student tanpa tunggakan - BISA daftar KRS
curl -X GET http://localhost:5000/api/billing/can-register/1

# Response (Status 200):
{
  "can_register": true,
  "message": "Mahasiswa bisa mendaftar KRS",
  "outstanding": 0
}
```

#### Test 2: Student CANNOT Register KRS (With Arrears)
```bash
# Student dengan tunggakan - TIDAK BISA daftar KRS
curl -X GET http://localhost:5000/api/billing/can-register/3

# Response (Status 403 Forbidden):
{
  "can_register": false,
  "message": "Mahasiswa memiliki tunggakan sebesar Rp 4,000,000",
  "outstanding": 4000000
}
```

#### Test 3: KRS Eligibility Report (All Students)
```bash
# Lihat semua student dan status KRS eligibility mereka
curl -X GET http://localhost:5000/api/billing/krs-eligibility-report

# Response:
{
  "timestamp": "2026-01-17T18:15:00.000000",
  "filter": "all",
  "summary": {
    "total_students": 3,
    "eligible_for_krs": 1,        # Bisa daftar KRS
    "blocked_from_krs": 2,        # Tidak bisa (ada tunggakan)
    "total_blocked_arrears": 10000000
  },
  "pagination": {
    "offset": 0,
    "limit": 100,
    "total": 3
  },
  "students": [
    {
      "student_id": 1,
      "nim": "2023001",
      "name": "John Doe",
      "program_studi": "Teknik Informatika",
      "eligible_for_krs": true,
      "outstanding": 0
    },
    {
      "student_id": 2,
      "nim": "2023002",
      "name": "Jane Smith",
      "program_studi": "Teknik Informatika",
      "eligible_for_krs": false,
      "outstanding": 5000000,
      "reason": "Has unpaid billing"
    },
    ...
  ]
}
```

#### Test 4: Check Only Blocked Students
```bash
# Lihat hanya student yang blocked dari KRS
curl -X GET "http://localhost:5000/api/billing/krs-eligibility-report?eligible=not_eligible"

# Response akan menampilkan hanya students dengan tunggakan
```

#### Test 5: Verify KRS Block in Student Profile
```bash
# Check apakah student bisa register KRS via dashboard
curl -X GET http://localhost:5000/api/dashboard/student-profile/3

# Response akan show status "can_register_krs": false jika ada tunggakan
```

---

## 🔄 Complete Testing Workflow

### Skenario 1: New Semester Billing Generation
```bash
# 1. Buat semester baru
curl -X POST http://localhost:5000/api/billing/generate/1

# 2. Check dashboard - should show pending billings
curl -X GET http://localhost:5000/api/dashboard/summary

# 3. Try KRS registration (should FAIL - has outstanding)
curl -X GET http://localhost:5000/api/billing/can-register/1

# Response: 403 Forbidden - has tunggakan
```

### Skenario 2: Partial Payment
```bash
# 1. Student 1 membayar sebagian (Rp 2,500,000 dari Rp 5,000,000)
curl -X POST http://localhost:5000/api/webhook/payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-2026-100",
    "reference_code": "PAY-00100-2026",
    "amount": 2500000,
    "status": "success",
    "timestamp": "2026-01-17T18:00:00",
    "billing_id": 1,
    "student_id": 1,
    "payment_method": "transfer"
  }'

# 2. Check billing status - should be PARTIAL
curl -X GET http://localhost:5000/api/billing/student/1

# 3. Try KRS registration (should still FAIL - outstanding > 0)
curl -X GET http://localhost:5000/api/billing/can-register/1

# Response: 403 Forbidden - masih punya tunggakan
```

### Skenario 3: Full Payment
```bash
# 1. Student 1 melunasi sisa pembayaran (Rp 2,500,000)
curl -X POST http://localhost:5000/api/webhook/payment \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-2026-101",
    "reference_code": "PAY-00101-2026",
    "amount": 2500000,
    "status": "success",
    "timestamp": "2026-01-17T18:05:00",
    "billing_id": 1,
    "student_id": 1,
    "payment_method": "transfer"
  }'

# 2. Check billing status - should be PAID
curl -X GET http://localhost:5000/api/billing/student/1

# 3. Try KRS registration (should SUCCESS - no outstanding)
curl -X GET http://localhost:5000/api/billing/can-register/1

# Response: 200 OK - bisa daftar KRS
```

---

## 📊 Expected Dashboard Metrics

After running all tests, dashboard should show:

```bash
curl -X GET http://localhost:5000/api/dashboard/summary

{
  "timestamp": "2026-01-17T18:10:00.000000",
  "metrics": {
    "total_active_students": 3,
    "total_billed": 15000000,
    "total_paid": 5000000,           # All payments from webhooks
    "total_outstanding": 10000000,    # Remaining unpaid
    "collection_rate": 33.33,         # 5M / 15M = 33.33%
    "students_with_overdue": 0        # No overdue (all within due date)
  }
}
```

---

## 🔍 Troubleshooting

### Issue: Scheduler tidak jalan
**Solution**: Check server logs
```bash
# Di terminal server
# Lihat pesan: "Scheduler started" dan "Billing scheduler configured successfully"
```

### Issue: Webhook tidak update billing
**Solution**: Check database
```bash
# Verify payment masuk ke database
sqlite3 spp_management.db
sqlite> SELECT * FROM payments ORDER BY created_at DESC LIMIT 5;
sqlite> SELECT id, student_id, status, remaining_amount FROM billings;
```

### Issue: KRS block tidak bekerja
**Solution**: Check outstanding calculation
```bash
# Verify outstanding query
curl -X GET http://localhost:5000/api/billing/outstanding | jq '.billings[] | select(.student_id == 3)'
```

---

## 📈 Performance Notes

- Dashboard queries optimized dengan `func.sum()` untuk aggregate calculations
- Scheduler runs di background - tidak blocking aplikasi
- Webhook processing asynchronous - immediate response 200 OK
- Real-time metrics pulled from database on each request

---

## ✅ Checklist Implementasi

- [x] Scheduler billing generation (hari 1 setiap bulan)
- [x] Scheduler penalty update (setiap hari 00:00)
- [x] Scheduler payment reminder (setiap hari 09:00)
- [x] Webhook payment endpoint (/api/webhook/payment)
- [x] Webhook test endpoint (/api/webhook/test)
- [x] Webhook health check (/api/webhook/health)
- [x] Webhook simulate payment (/api/webhook/simulate-payment)
- [x] Webhook test all students (/api/webhook/test-all-students)
- [x] Dashboard summary (real-time metrics)
- [x] Dashboard billing breakdown (/api/dashboard/billing-breakdown)
- [x] Dashboard students status (/api/dashboard/students-status)
- [x] Dashboard daily report (/api/dashboard/daily-report)
- [x] Financial report (analytics)
- [x] Student profile (detailed view)
- [x] Program studi statistics
- [x] KRS eligibility check (can-register endpoint)
- [x] KRS eligibility report (/api/billing/krs-eligibility-report)
- [x] KRS block for arrears (403 response)

---

## 🎯 Quick Reference - All Endpoints

### Billing Endpoints (8)
```
GET    /api/billing/student/<student_id>
GET    /api/billing/can-register/<student_id>          (403 if has arrears)
GET    /api/billing/outstanding
GET    /api/billing/krs-eligibility-report              (NEW - detailed KRS check)
POST   /api/billing/generate/<semester_id>
POST   /api/billing/update-penalty/<billing_id>
```

### Payment Endpoints (4)
```
GET    /api/payment/history/<student_id>
GET    /api/payment/statistics
GET    /api/payment/<payment_id>
POST   /api/payment/process
```

### Dashboard Endpoints (7)
```
GET    /api/dashboard/summary                           (real-time metrics)
GET    /api/dashboard/billing-breakdown                 (NEW - status breakdown)
GET    /api/dashboard/students-status                   (NEW - per student report)
GET    /api/dashboard/daily-report                      (NEW - today's metrics)
GET    /api/dashboard/financial-report?days=30          (analytics)
GET    /api/dashboard/program-studi-stats               (per program studi)
GET    /api/dashboard/student-profile/<student_id>
```

### Webhook Endpoints (5)
```
POST   /api/webhook/payment                             (production endpoint)
POST   /api/webhook/test                                (development only)
POST   /api/webhook/simulate-payment                    (NEW - test payment)
POST   /api/webhook/test-all-students                   (NEW - bulk test)
GET    /api/webhook/health                              (status check)
```

---

**Last Updated**: 2026-01-17  
**System**: SPP Management System - MINGGU 11  
**Status**: ✅ All 4 Features Active & Tested
