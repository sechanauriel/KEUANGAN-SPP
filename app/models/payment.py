# app/models/payment.py
from app.models.base import db
from datetime import datetime
import secrets

class Payment(db.Model):
    """Model untuk data pembayaran"""
    __tablename__ = 'payments'
    
    # Status pembayaran
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_FAILED = 'failed'
    
    VALID_STATUSES = [STATUS_PENDING, STATUS_CONFIRMED, STATUS_FAILED]
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    billing_id = db.Column(db.Integer, db.ForeignKey('billings.id'), nullable=False, index=True)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    
    # Transaction details
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Dari payment gateway
    reference_code = db.Column(db.String(50), unique=True, nullable=False)  # Internal reference
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default=STATUS_PENDING)
    
    # Gateway information
    gateway_name = db.Column(db.String(50))  # e.g., "Midtrans", "BCA Virtual Account"
    gateway_response = db.Column(db.JSON)  # Response dari payment gateway
    
    payment_date = db.Column(db.DateTime)
    confirmation_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payment_method = db.relationship('PaymentMethod', backref='payments')
    
    def __repr__(self):
        return f'<Payment {self.reference_code} - {self.status}>'
    
    @staticmethod
    def generate_reference_code():
        """Generate reference code unik untuk pembayaran"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = secrets.token_hex(3).upper()
        return f"PAY{timestamp}{random_suffix}"


class PaymentReconciliation(db.Model):
    """Model untuk rekonsiliasi pembayaran dari payment gateway"""
    __tablename__ = 'payment_reconciliations'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    gateway_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # synced, failed, pending
    gateway_response = db.Column(db.JSON)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaymentReconciliation {self.gateway_name} - {self.status}>'
