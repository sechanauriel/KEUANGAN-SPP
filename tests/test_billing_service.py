# tests/test_billing_service.py
import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models.student import Student, ProgramStudi
from app.models.billing import Billing, Semester
from app.services.billing_service import BillingService

class TestBillingService(unittest.TestCase):
    """Test cases untuk Billing Service"""
    
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
        db.session.commit()
        
        # Create students
        for i in range(3):
            student = Student(
                nim=f'2021000{i+1}',
                name=f'Test Student {i+1}',
                email=f'student{i+1}@test.com',
                program_studi_id=ps.id,
                status='active'
            )
            db.session.add(student)
        db.session.commit()
        
        # Create semester
        semester = Semester(
            name='2023/2024-Ganjil',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=120),
            is_active=True
        )
        db.session.add(semester)
        db.session.commit()
    
    def test_generate_billing(self):
        """Test billing generation"""
        with self.app.app_context():
            billing_service = BillingService()
            semester = Semester.query.first()
            
            result = billing_service.generate_billing_for_semester(semester.id)
            
            self.assertTrue(result['success'])
            self.assertEqual(result['created_count'], 3)
            
            # Verify billings created
            billings = Billing.query.all()
            self.assertEqual(len(billings), 3)
            
            # Check billing details
            for billing in billings:
                self.assertEqual(billing.total_amount, 5000000)
                self.assertEqual(billing.status, Billing.STATUS_UNPAID)
    
    def test_can_register_krs_no_outstanding(self):
        """Test KRS registration when no outstanding"""
        with self.app.app_context():
            student = Student.query.first()
            
            billing_service = BillingService()
            result = billing_service.can_student_register_krs(student.id)
            
            self.assertTrue(result['can_register'])
            self.assertEqual(result['outstanding'], 0)
    
    def test_can_register_krs_with_outstanding(self):
        """Test KRS registration when has outstanding"""
        with self.app.app_context():
            student = Student.query.first()
            
            # Create unpaid billing
            billing = Billing(
                student_id=student.id,
                semester='2023/2024-Ganjil',
                total_amount=5000000,
                remaining_amount=5000000,
                due_date=datetime.utcnow() + timedelta(days=14),
                status=Billing.STATUS_UNPAID
            )
            db.session.add(billing)
            db.session.commit()
            
            billing_service = BillingService()
            result = billing_service.can_student_register_krs(student.id)
            
            self.assertFalse(result['can_register'])
            self.assertEqual(result['outstanding'], 5000000)
    
    def test_calculate_penalty(self):
        """Test penalty calculation"""
        with self.app.app_context():
            billing = Billing.query.first()
            if not billing:
                # Create billing if not exists
                student = Student.query.first()
                billing = Billing(
                    student_id=student.id,
                    semester='2023/2024-Ganjil',
                    total_amount=5000000,
                    remaining_amount=5000000,
                    due_date=datetime.utcnow() - timedelta(days=10),
                    status=Billing.STATUS_UNPAID
                )
                db.session.add(billing)
                db.session.commit()
            
            billing_service = BillingService()
            result = billing_service.calculate_and_update_penalty(
                billing.id,
                penalty_per_day=10000,
                max_penalty=500000
            )
            
            self.assertTrue(result['success'])
            self.assertGreater(result['penalty'], 0)

if __name__ == '__main__':
    unittest.main()
