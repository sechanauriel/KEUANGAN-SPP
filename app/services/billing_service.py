# app/services/billing_service.py
from datetime import datetime, timedelta
from app.models import db
from app.models.student import Student, ProgramStudi
from app.models.billing import Billing, Semester
from app.utils.logger import logger

class BillingService:
    """Service untuk mengelola billing/tagihan SPP"""
    
    def __init__(self, app=None):
        self.app = app
        
    def generate_billing_for_semester(self, semester_id, billing_due_days=14):
        """
        Generate billing untuk semua mahasiswa aktif di semester tertentu
        
        Args:
            semester_id: ID semester
            billing_due_days: Jumlah hari untuk due date (default: 14 hari)
            
        Returns:
            dict: {success: bool, message: str, created_count: int, failed_count: int}
        """
        try:
            semester = Semester.query.get(semester_id)
            if not semester:
                return {
                    'success': False,
                    'message': f'Semester dengan ID {semester_id} tidak ditemukan'
                }
            
            # Ambil semua mahasiswa aktif
            active_students = Student.query.filter_by(status='active').all()
            
            created_count = 0
            failed_count = 0
            
            for student in active_students:
                try:
                    # Cek apakah sudah ada billing untuk semester ini
                    existing_billing = Billing.query.filter_by(
                        student_id=student.id,
                        semester=semester.name
                    ).first()
                    
                    if existing_billing:
                        continue
                    
                    # Ambil SPP amount dari program studi
                    spp_amount = student.program_studi.spp_amount
                    
                    # Calculate due date
                    due_date = datetime.utcnow() + timedelta(days=billing_due_days)
                    
                    # Create billing
                    billing = Billing(
                        student_id=student.id,
                        semester=semester.name,
                        total_amount=spp_amount,
                        remaining_amount=spp_amount,
                        due_date=due_date,
                        status=Billing.STATUS_UNPAID
                    )
                    
                    db.session.add(billing)
                    created_count += 1
                    
                except Exception as e:
                    logger.error(f"Error creating billing for student {student.nim}: {str(e)}")
                    failed_count += 1
            
            db.session.commit()
            
            message = f"Berhasil generate billing untuk {created_count} mahasiswa"
            if failed_count > 0:
                message += f", {failed_count} gagal"
            
            logger.info(message)
            
            return {
                'success': True,
                'message': message,
                'created_count': created_count,
                'failed_count': failed_count
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Error generating billing: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
    
    def calculate_and_update_penalty(self, billing_id, penalty_per_day, max_penalty):
        """
        Hitung dan update denda keterlambatan
        
        Args:
            billing_id: ID billing
            penalty_per_day: Denda per hari (dalam Rupiah)
            max_penalty: Denda maksimum
            
        Returns:
            dict: {success: bool, billing: Billing, penalty: int}
        """
        try:
            billing = Billing.query.get(billing_id)
            if not billing:
                return {'success': False, 'message': 'Billing tidak ditemukan'}
            
            # Calculate penalty
            penalty = billing.calculate_penalty(penalty_per_day, max_penalty)
            billing.penalty = penalty
            
            # Update status jika overdue
            if billing.is_overdue and billing.status != Billing.STATUS_PAID:
                billing.status = Billing.STATUS_OVERDUE
            
            db.session.commit()
            
            return {
                'success': True,
                'billing': billing,
                'penalty': penalty
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error calculating penalty: {str(e)}")
            return {
                'success': False,
                'message': str(e)
            }
    
    def can_student_register_krs(self, student_id):
        """
        Cek apakah mahasiswa bisa mendaftar KRS (tidak ada tunggakan)
        
        Args:
            student_id: ID mahasiswa
            
        Returns:
            dict: {can_register: bool, message: str, outstanding: int}
        """
        student = Student.query.get(student_id)
        if not student:
            return {
                'can_register': False,
                'message': 'Mahasiswa tidak ditemukan',
                'outstanding': 0
            }
        
        # Cek tunggakan yang belum lunas
        outstanding_billings = Billing.query.filter(
            Billing.student_id == student_id,
            Billing.status.in_([Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL, Billing.STATUS_OVERDUE])
        ).all()
        
        total_outstanding = sum(b.remaining_amount for b in outstanding_billings)
        
        if total_outstanding > 0:
            return {
                'can_register': False,
                'message': f'Mahasiswa memiliki tunggakan sebesar Rp {total_outstanding:,}',
                'outstanding': total_outstanding
            }
        
        return {
            'can_register': True,
            'message': 'Mahasiswa bisa mendaftar KRS',
            'outstanding': 0
        }
    
    def get_billing_summary(self, student_id):
        """
        Dapatkan ringkasan billing untuk satu mahasiswa
        
        Args:
            student_id: ID mahasiswa
            
        Returns:
            dict: {student, total_billed, total_paid, total_outstanding, billings}
        """
        student = Student.query.get(student_id)
        if not student:
            return {'error': 'Mahasiswa tidak ditemukan'}
        
        billings = Billing.query.filter_by(student_id=student_id).all()
        
        total_billed = sum(b.total_amount for b in billings)
        total_paid = sum(b.paid_amount for b in billings)
        total_outstanding = sum(b.remaining_amount for b in billings)
        
        return {
            'student': student,
            'total_billed': total_billed,
            'total_paid': total_paid,
            'total_outstanding': total_outstanding,
            'billings': billings
        }
