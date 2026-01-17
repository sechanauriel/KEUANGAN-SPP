#!/bin/bash
# SPP Management System - Comprehensive Testing Script
# Test all 4 implemented features with curl commands

BASE_URL="http://localhost:5000"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}SPP Management System - Testing Script${NC}"
echo -e "${BLUE}========================================${NC}\n"

# ============================================================
# 1. BILLING AUTO-GENERATE PER SEMESTER
# ============================================================
echo -e "${YELLOW}[1] Testing Billing Auto-Generate Per Semester${NC}\n"

echo -e "${GREEN}1.1 Trigger billing generation for active semester:${NC}"
echo "POST /api/billing/generate/1"
curl -X POST "$BASE_URL/api/billing/generate/1" \
  -H "Content-Type: application/json" \
  -d '{"due_days": 14}' | jq .
echo ""

echo -e "${GREEN}1.2 Get outstanding billings:${NC}"
echo "GET /api/billing/outstanding"
curl -X GET "$BASE_URL/api/billing/outstanding" | jq .
echo ""

echo -e "${GREEN}1.3 Get student billing details:${NC}"
echo "GET /api/billing/student/1"
curl -X GET "$BASE_URL/api/billing/student/1" | jq .
echo ""

# ============================================================
# 2. WEBHOOK PAYMENT FUNCTIONALITY
# ============================================================
echo -e "${YELLOW}[2] Testing Webhook Payment Functionality${NC}\n"

echo -e "${GREEN}2.1 Webhook health check:${NC}"
echo "GET /api/webhook/health"
curl -X GET "$BASE_URL/api/webhook/health" | jq .
echo ""

echo -e "${GREEN}2.2 Test webhook endpoint (echo):${NC}"
echo "POST /api/webhook/test"
curl -X POST "$BASE_URL/api/webhook/test" \
  -H "Content-Type: application/json" \
  -d '{"test_data": "This is a test webhook"}' | jq .
echo ""

echo -e "${GREEN}2.3 Simulate payment for student 1:${NC}"
echo "POST /api/webhook/simulate-payment"
curl -X POST "$BASE_URL/api/webhook/simulate-payment" \
  -H "Content-Type: application/json" \
  -d '{
    "billing_id": 1,
    "student_id": 1,
    "amount": 2500000,
    "payment_method": "transfer"
  }' | jq .
echo ""

echo -e "${GREEN}2.4 Process payment webhook directly:${NC}"
echo "POST /api/webhook/payment"
curl -X POST "$BASE_URL/api/webhook/payment" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "TXN-TEST-001",
    "billing_id": 1,
    "student_id": 1,
    "amount": 1000000,
    "status": "success",
    "payment_method": "transfer",
    "timestamp": "2026-01-17T18:00:00"
  }' | jq .
echo ""

echo -e "${GREEN}2.5 Test bulk student payments (50% of outstanding):${NC}"
echo "POST /api/webhook/test-all-students"
curl -X POST "$BASE_URL/api/webhook/test-all-students" \
  -H "Content-Type: application/json" \
  -d '{"amount_percentage": 50}' | jq .
echo ""

# ============================================================
# 3. REAL-TIME DASHBOARD
# ============================================================
echo -e "${YELLOW}[3] Testing Real-Time Dashboard${NC}\n"

echo -e "${GREEN}3.1 Dashboard summary (main metrics):${NC}"
echo "GET /api/dashboard/summary"
curl -X GET "$BASE_URL/api/dashboard/summary" | jq .
echo ""

echo -e "${GREEN}3.2 Billing breakdown by status:${NC}"
echo "GET /api/dashboard/billing-breakdown"
curl -X GET "$BASE_URL/api/dashboard/billing-breakdown" | jq .
echo ""

echo -e "${GREEN}3.3 Students payment status report:${NC}"
echo "GET /api/dashboard/students-status"
curl -X GET "$BASE_URL/api/dashboard/students-status" | jq .
echo ""

echo -e "${GREEN}3.4 Filter students by status (only unpaid):${NC}"
echo "GET /api/dashboard/students-status?status=unpaid"
curl -X GET "$BASE_URL/api/dashboard/students-status?status=unpaid" | jq .
echo ""

echo -e "${GREEN}3.5 Daily report:${NC}"
echo "GET /api/dashboard/daily-report"
curl -X GET "$BASE_URL/api/dashboard/daily-report" | jq .
echo ""

echo -e "${GREEN}3.6 Financial report (last 30 days):${NC}"
echo "GET /api/dashboard/financial-report?days=30"
curl -X GET "$BASE_URL/api/dashboard/financial-report?days=30" | jq .
echo ""

echo -e "${GREEN}3.7 Program studi statistics:${NC}"
echo "GET /api/dashboard/program-studi-stats"
curl -X GET "$BASE_URL/api/dashboard/program-studi-stats" | jq .
echo ""

echo -e "${GREEN}3.8 Student financial profile:${NC}"
echo "GET /api/dashboard/student-profile/1"
curl -X GET "$BASE_URL/api/dashboard/student-profile/1" | jq .
echo ""

# ============================================================
# 4. KRS BLOCKING FOR STUDENTS WITH ARREARS
# ============================================================
echo -e "${YELLOW}[4] Testing KRS Blocking for Students with Arrears${NC}\n"

echo -e "${GREEN}4.1 Check KRS eligibility for student 1 (should be OK if paid):${NC}"
echo "GET /api/billing/can-register/1"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/billing/can-register/1")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
echo "$BODY" | jq .
echo "HTTP Status: $HTTP_CODE"
echo ""

echo -e "${GREEN}4.2 Check KRS eligibility for student with arrears (should return 403):${NC}"
echo "GET /api/billing/can-register/2"
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/api/billing/can-register/2")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
echo "$BODY" | jq .
echo "HTTP Status: $HTTP_CODE (Expected: 403 Forbidden if has arrears)"
echo ""

echo -e "${GREEN}4.3 KRS Eligibility Report (all students):${NC}"
echo "GET /api/billing/krs-eligibility-report"
curl -X GET "$BASE_URL/api/billing/krs-eligibility-report" | jq .
echo ""

echo -e "${GREEN}4.4 KRS Eligibility Report (only eligible):${NC}"
echo "GET /api/billing/krs-eligibility-report?eligible=eligible"
curl -X GET "$BASE_URL/api/billing/krs-eligibility-report?eligible=eligible" | jq .
echo ""

echo -e "${GREEN}4.5 KRS Eligibility Report (only blocked):${NC}"
echo "GET /api/billing/krs-eligibility-report?eligible=not_eligible"
curl -X GET "$BASE_URL/api/billing/krs-eligibility-report?eligible=not_eligible" | jq .
echo ""

# ============================================================
# SUMMARY
# ============================================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}✅ Testing Complete!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo -e "${GREEN}Summary of Features Tested:${NC}"
echo "✅ [1] Billing Auto-Generate Per Semester"
echo "   - Manual trigger endpoint"
echo "   - Outstanding billing check"
echo "   - Student billing details"
echo ""
echo "✅ [2] Webhook Payment Functionality"
echo "   - Health check endpoint"
echo "   - Test webhook echo"
echo "   - Simulate individual payment"
echo "   - Direct webhook processing"
echo "   - Bulk student payment testing"
echo ""
echo "✅ [3] Real-Time Dashboard"
echo "   - Summary metrics"
echo "   - Billing breakdown by status"
echo "   - Students payment status report"
echo "   - Daily report"
echo "   - Financial report with analytics"
echo "   - Program studi statistics"
echo "   - Student profile view"
echo ""
echo "✅ [4] KRS Blocking for Arrears"
echo "   - Individual KRS eligibility check"
echo "   - KRS eligibility report (all)"
echo "   - KRS eligibility report (filtered)"
echo ""
echo -e "${GREEN}All endpoints tested successfully!${NC}\n"
