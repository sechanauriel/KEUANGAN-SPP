# app/models/payment_method.py
from app.models.base import db
from datetime import datetime

class PaymentMethod(db.Model):
    """Model untuk metode pembayaran yang tersedia"""
    __tablename__ = 'payment_methods'
    
    # Jenis metode pembayaran
    METHOD_BANK_TRANSFER = 'bank_transfer'
    METHOD_VIRTUAL_ACCOUNT = 'virtual_account'
    METHOD_E_WALLET = 'e_wallet'
    METHOD_CREDIT_CARD = 'credit_card'
    METHOD_CASH = 'cash'
    
    VALID_METHODS = [
        METHOD_BANK_TRANSFER,
        METHOD_VIRTUAL_ACCOUNT,
        METHOD_E_WALLET,
        METHOD_CREDIT_CARD,
        METHOD_CASH
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "BCA Transfer", "GCash"
    method_type = db.Column(db.String(50), nullable=False)  # Jenis metode
    provider = db.Column(db.String(100))  # e.g., "BCA", "GCash"
    is_active = db.Column(db.Boolean, default=True)
    gateway_code = db.Column(db.String(50))  # Kode untuk payment gateway
    description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaymentMethod {self.name}>'
