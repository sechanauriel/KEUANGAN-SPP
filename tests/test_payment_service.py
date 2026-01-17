# tests/test_payment_service.py
import unittest
from datetime import datetime
from app import create_app, db
from app.models.student import Student, ProgramStudi
from app.models.billing import Billing, Semester
from app.models.payment import Payment
from app.models.payment_method import PaymentMethod
from app.services.payment_service import PaymentService

class TestPaymentService(unittest.TestCase):
    """Test cases untuk Payment Service"""
    
    def setUp(self):
        """Setup test database"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self.setup_test_data()
    
    def tearDown(self):
        """Cleanup test database"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def setup_test_data(self):
        """Create test data"""
        # Create program studi
        ps = ProgramStudi(name='Teknik Informatika', code='TI', spp_amount=5000000)
        db.session.add(ps)
        
        # Create payment method
        pm = PaymentMethod(
            name='Test Payment',
            method_type='bank_transfer',
            provider='BCA'
        )
        db.session.add(pm)
        db.session.commit()
        
        # Create student
        student = Student(
            nim='2021000001',
            name='Test Student',
            email='student@test.com',
            program_studi_id=ps.id,
            status='active'
        )
        db.session.add(student)
        db.session.commit()
        
        # Create billing
        billing = Billing(
            student_id=student.id,
            semester='2023/2024-Ganjil',
            total_amount=5000000,
            remaining_amount=5000000,
            due_date=datetime.utcnow(),
            status=Billing.STATUS_UNPAID
        )
        db.session.add(billing)
        db.session.commit()
    
    def test_process_payment_full(self):
        """Test processing full payment"""
        with self.app.app_context():
            billing = Billing.query.first()
            payment_method = PaymentMethod.query.first()
            
            payment_service = PaymentService()
            result = payment_service.process_payment(
                billing_id=billing.id,
                amount=5000000,
                payment_method_id=payment_method.id,
                transaction_id='TXN001'
            )
            
            self.assertTrue(result['success'])
            
            # Check payment created
            payment = Payment.query.first()
            self.assertIsNotNone(payment)
            self.assertEqual(payment.amount, 5000000)
            self.assertEqual(payment.status, Payment.STATUS_CONFIRMED)
            
            # Check billing updated
            billing = Billing.query.get(billing.id)
            self.assertEqual(billing.paid_amount, 5000000)
            self.assertEqual(billing.remaining_amount, 0)
            self.assertEqual(billing.status, Billing.STATUS_PAID)
    
    def test_process_payment_partial(self):
        """Test processing partial payment"""
        with self.app.app_context():
            billing = Billing.query.first()
            payment_method = PaymentMethod.query.first()
            
            payment_service = PaymentService()
            result = payment_service.process_payment(
                billing_id=billing.id,
                amount=2500000,
                payment_method_id=payment_method.id,
                transaction_id='TXN001'
            )
            
            self.assertTrue(result['success'])
            
            # Check billing updated
            billing = Billing.query.get(billing.id)
            self.assertEqual(billing.paid_amount, 2500000)
            self.assertEqual(billing.remaining_amount, 2500000)
            self.assertEqual(billing.status, Billing.STATUS_PARTIAL)

if __name__ == '__main__':
    unittest.main()
