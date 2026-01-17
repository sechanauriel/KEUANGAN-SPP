# app/services/payment_service.py
from datetime import datetime
import hashlib
import hmac
from app.models import db
from app.models.payment import Payment, PaymentReconciliation
from app.models.billing import Billing
from app.utils.logger import logger

class PaymentService:
    """Service untuk mengelola pembayaran dan webhook handling"""
    
    def __init__(self, app=None):
        self.app = app
        
    def process_payment(self, billing_id, amount, payment_method_id, transaction_id, gateway_name='manual'):
        """
        Proses pembayaran untuk billing tertentu
        
        Args:
            billing_id: ID billing
            amount: Jumlah pembayaran
            payment_method_id: ID metode pembayaran
            transaction_id: ID transaksi dari payment gateway
            gateway_name: Nama payment gateway
            
        Returns:
            dict: {success: bool, message: str, payment: Payment, billing: Billing}
        """
        try:
            billing = Billing.query.get(billing_id)
            if not billing:
                return {'success': False, 'message': 'Billing tidak ditemukan'}
            
            if amount <= 0:
                return {'success': False, 'message': 'Jumlah pembayaran harus lebih dari 0'}
            
            # Create payment record
            payment = Payment(
                student_id=billing.student_id,
                billing_id=billing_id,
                payment_method_id=payment_method_id,
                transaction_id=transaction_id,
                reference_code=Payment.generate_reference_code(),
                amount=amount,
                gateway_name=gateway_name,
                status=Payment.STATUS_CONFIRMED,
                payment_date=datetime.utcnow(),
                confirmation_date=datetime.utcnow()
            )
            
            # Update billing
            billing.paid_amount += amount
            billing.remaining_amount = billing.total_amount - billing.paid_amount
            billing.last_payment_date = datetime.utcnow()
            
            # Update status
            if billing.paid_amount == 0:
                billing.status = Billing.STATUS_UNPAID
            elif billing.paid_amount < billing.total_amount:
                billing.status = Billing.STATUS_PARTIAL
            else:
                billing.status = Billing.STATUS_PAID
            
            db.session.add(payment)
            db.session.commit()
            
            logger.info(f"Payment processed: {payment.reference_code} for billing {billing_id}")
            
            return {
                'success': True,
                'message': f'Pembayaran sebesar Rp {amount:,} berhasil dicatat',
                'payment': payment,
                'billing': billing
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Error processing payment: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'message': error_msg}
    
    def handle_webhook(self, payload, webhook_secret):
        """
        Handle webhook notification dari payment gateway
        
        Args:
            payload: Data dari webhook (JSON)
            webhook_secret: Secret key untuk verifikasi signature
            
        Returns:
            dict: {success: bool, message: str, payment: Payment}
        """
        try:
            # Verifikasi signature
            if not self._verify_webhook_signature(payload, webhook_secret):
                logger.warning("Webhook signature verification failed")
                return {
                    'success': False,
                    'message': 'Webhook signature verification failed',
                    'status_code': 401
                }
            
            # Extract data
            transaction_id = payload.get('transaction_id')
            reference_code = payload.get('reference_code')
            amount = payload.get('amount')
            status = payload.get('status')  # success, failed, pending
            
            if not all([transaction_id, reference_code, amount, status]):
                return {
                    'success': False,
                    'message': 'Invalid webhook payload',
                    'status_code': 400
                }
            
            # Cari payment berdasarkan reference code
            payment = Payment.query.filter_by(reference_code=reference_code).first()
            if not payment:
                return {
                    'success': False,
                    'message': 'Payment not found',
                    'status_code': 404
                }
            
            # Update payment status
            if status == 'success':
                payment.status = Payment.STATUS_CONFIRMED
                payment.confirmation_date = datetime.utcnow()
                
                # Process the payment
                result = self.process_payment(
                    payment.billing_id,
                    amount,
                    payment.payment_method_id,
                    transaction_id,
                    'webhook'
                )
                
                if not result['success']:
                    payment.status = Payment.STATUS_FAILED
                    db.session.commit()
                    return result
                    
            elif status == 'failed':
                payment.status = Payment.STATUS_FAILED
                
            payment.gateway_response = payload
            db.session.commit()
            
            # Log webhook processing
            reconciliation = PaymentReconciliation(
                payment_id=payment.id,
                gateway_name=payment.gateway_name,
                status='synced',
                gateway_response=payload
            )
            db.session.add(reconciliation)
            db.session.commit()
            
            logger.info(f"Webhook processed for payment {reference_code}: {status}")
            
            return {
                'success': True,
                'message': 'Webhook processed successfully',
                'payment': payment,
                'status_code': 200
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Error handling webhook: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg,
                'status_code': 500
            }
    
    @staticmethod
    def _verify_webhook_signature(payload, webhook_secret):
        """
        Verify webhook signature untuk memastikan authenticity
        
        Args:
            payload: Webhook payload
            webhook_secret: Secret key
            
        Returns:
            bool: True if signature is valid
        """
        # Implementation tergantung payment gateway
        # Contoh sederhana menggunakan HMAC-SHA256
        
        signature = payload.pop('signature', None) if isinstance(payload, dict) else None
        
        if not signature:
            return False
        
        # Create message string
        message = str(payload) if isinstance(payload, dict) else str(payload)
        
        # Calculate expected signature
        expected_signature = hmac.new(
            webhook_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures (constant time comparison)
        return hmac.compare_digest(signature, expected_signature)
    
    def get_payment_history(self, student_id, limit=10):
        """
        Dapatkan riwayat pembayaran untuk satu mahasiswa
        
        Args:
            student_id: ID mahasiswa
            limit: Jumlah record
            
        Returns:
            list: Daftar pembayaran
        """
        payments = Payment.query.filter_by(student_id=student_id)\
            .order_by(Payment.created_at.desc())\
            .limit(limit)\
            .all()
        
        return payments
    
    def get_payment_statistics(self, start_date=None, end_date=None):
        """
        Dapatkan statistik pembayaran
        
        Args:
            start_date: Tanggal mulai
            end_date: Tanggal akhir
            
        Returns:
            dict: Statistik pembayaran
        """
        from sqlalchemy import func
        
        query = Payment.query.filter_by(status=Payment.STATUS_CONFIRMED)
        
        if start_date:
            query = query.filter(Payment.confirmation_date >= start_date)
        if end_date:
            query = query.filter(Payment.confirmation_date <= end_date)
        
        payments = query.all()
        
        total_payments = len(payments)
        total_amount = sum(p.amount for p in payments)
        average_amount = total_amount / total_payments if total_payments > 0 else 0
        
        return {
            'total_payments': total_payments,
            'total_amount': total_amount,
            'average_amount': average_amount,
            'payments': payments
        }
