# app/services/ai_service.py
from datetime import datetime, timedelta
from app.models.student import Student
from app.models.billing import Billing
from app.models.payment import Payment
import json

class AIFinancialService:
    """Service untuk AI-powered financial reporting dan insights"""
    
    def __init__(self, app=None):
        self.app = app
        
    def generate_financial_report(self, start_date=None, end_date=None):
        """
        Generate laporan keuangan dengan analisis AI
        
        Args:
            start_date: Tanggal mulai
            end_date: Tanggal akhir (default: hari ini)
            
        Returns:
            dict: Laporan dengan insights
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Ambil data pembayaran
        payments = Payment.query.filter(
            Payment.status == 'confirmed',
            Payment.confirmation_date >= start_date,
            Payment.confirmation_date <= end_date
        ).all()
        
        # Ambil data billing
        billings = Billing.query.filter(
            Billing.created_at >= start_date,
            Billing.created_at <= end_date
        ).all()
        
        # Calculate metrics
        total_revenue = sum(p.amount for p in payments)
        num_payments = len(payments)
        average_payment = total_revenue / num_payments if num_payments > 0 else 0
        
        total_billed = sum(b.total_amount for b in billings)
        collection_rate = (total_revenue / total_billed * 100) if total_billed > 0 else 0
        
        # Get outstanding billings
        outstanding_billings = Billing.query.filter(
            Billing.status.in_(['unpaid', 'partial', 'overdue'])
        ).order_by(Billing.remaining_amount.desc()).limit(10).all()
        
        # Get overdue billings
        overdue_billings = Billing.query.filter(
            Billing.status == 'overdue'
        ).all()
        
        total_overdue = sum(b.remaining_amount for b in overdue_billings)
        
        # Build report
        report = {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'revenue_metrics': {
                'total_revenue': total_revenue,
                'total_payments': num_payments,
                'average_payment': average_payment,
                'total_billed': total_billed,
                'collection_rate': round(collection_rate, 2)
            },
            'outstanding': {
                'total_outstanding': sum(b.remaining_amount for b in outstanding_billings),
                'total_overdue': total_overdue,
                'num_overdue_students': len(overdue_billings)
            },
            'top_outstanding_billings': [
                {
                    'student_nim': b.student.nim,
                    'student_name': b.student.name,
                    'semester': b.semester,
                    'amount': b.remaining_amount,
                    'days_overdue': b.days_overdue if b.is_overdue else 0,
                    'status': b.status
                }
                for b in outstanding_billings
            ],
            'ai_insights': self._generate_insights(
                total_revenue, 
                collection_rate,
                total_overdue,
                len(overdue_billings),
                num_payments
            )
        }
        
        return report
    
    def _generate_insights(self, total_revenue, collection_rate, total_overdue, 
                          num_overdue, num_payments):
        """
        Generate AI insights dari financial data
        
        Args:
            total_revenue: Total pendapatan
            collection_rate: Persentase pengumpulan
            total_overdue: Total tunggakan
            num_overdue: Jumlah siswa dengan tunggakan
            num_payments: Jumlah pembayaran
            
        Returns:
            dict: Insights dan rekomendasi
        """
        insights = []
        recommendations = []
        
        # Revenue analysis
        if total_revenue == 0:
            insights.append("⚠️ Tidak ada pembayaran dalam periode ini")
            recommendations.append("Kirim reminder ke semua mahasiswa")
        elif total_revenue < 50000000:
            insights.append(f"📊 Pendapatan masih rendah: Rp {total_revenue:,}")
            recommendations.append("Lakukan follow-up ke mahasiswa yang belum membayar")
        else:
            insights.append(f"✅ Pendapatan sehat: Rp {total_revenue:,}")
        
        # Collection rate analysis
        if collection_rate < 50:
            insights.append(f"🔴 Tingkat pengumpulan rendah: {collection_rate:.1f}%")
            recommendations.append("Butuh tindakan intensif untuk pengumpulan")
        elif collection_rate < 80:
            insights.append(f"🟡 Tingkat pengumpulan sedang: {collection_rate:.1f}%")
            recommendations.append("Tingkatkan komunikasi dengan mahasiswa")
        else:
            insights.append(f"🟢 Tingkat pengumpulan baik: {collection_rate:.1f}%")
        
        # Overdue analysis
        if num_overdue > 0:
            insights.append(f"⚠️ {num_overdue} mahasiswa dengan tunggakan")
            insights.append(f"💰 Total tunggakan: Rp {total_overdue:,}")
            recommendations.append(f"Prioritas: Kirim reminder ke {min(num_overdue, 5)} mahasiswa dengan tunggakan terbesar")
        else:
            insights.append("✅ Tidak ada tunggakan - Situasi baik!")
        
        # Payment frequency
        if num_payments > 0:
            insights.append(f"📈 {num_payments} transaksi pembayaran tercatat")
        
        return {
            'insights': insights,
            'recommendations': recommendations,
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def get_student_financial_profile(self, student_id):
        """
        Dapatkan profil finansial lengkap untuk satu mahasiswa
        
        Args:
            student_id: ID mahasiswa
            
        Returns:
            dict: Profil finansial dengan insights
        """
        student = Student.query.get(student_id)
        if not student:
            return {'error': 'Mahasiswa tidak ditemukan'}
        
        billings = Billing.query.filter_by(student_id=student_id).all()
        payments = Payment.query.filter_by(student_id=student_id).all()
        
        total_billed = sum(b.total_amount for b in billings)
        total_paid = sum(b.paid_amount for b in billings)
        total_outstanding = sum(b.remaining_amount for b in billings)
        
        overdue_billings = [b for b in billings if b.is_overdue]
        total_overdue = sum(b.remaining_amount for b in overdue_billings)
        
        profile = {
            'student': {
                'nim': student.nim,
                'name': student.name,
                'email': student.email,
                'program_studi': student.program_studi.name
            },
            'financial_summary': {
                'total_billed': total_billed,
                'total_paid': total_paid,
                'total_outstanding': total_outstanding,
                'payment_percentage': (total_paid / total_billed * 100) if total_billed > 0 else 0
            },
            'overdue_info': {
                'has_overdue': len(overdue_billings) > 0,
                'num_overdue_billings': len(overdue_billings),
                'total_overdue_amount': total_overdue
            },
            'recent_payments': [
                {
                    'date': p.payment_date.isoformat(),
                    'amount': p.amount,
                    'reference': p.reference_code,
                    'method': p.payment_method.name
                }
                for p in sorted(payments, key=lambda x: x.payment_date, reverse=True)[:5]
            ],
            'billing_details': [
                {
                    'semester': b.semester,
                    'total': b.total_amount,
                    'paid': b.paid_amount,
                    'remaining': b.remaining_amount,
                    'status': b.status,
                    'due_date': b.due_date.isoformat(),
                    'days_overdue': b.days_overdue if b.is_overdue else 0
                }
                for b in billings
            ]
        }
        
        return profile
    
    def export_report_to_json(self, report):
        """
        Export report ke format JSON
        
        Args:
            report: Report dictionary
            
        Returns:
            str: JSON string
        """
        return json.dumps(report, indent=2, default=str)
