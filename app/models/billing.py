# app/models/billing.py
from app.models.base import db
from datetime import datetime

class Billing(db.Model):
    """Model untuk data tagihan SPP"""
    __tablename__ = 'billings'
    
    # Status: unpaid, partial, paid, overdue
    STATUS_UNPAID = 'unpaid'
    STATUS_PARTIAL = 'partial'
    STATUS_PAID = 'paid'
    STATUS_OVERDUE = 'overdue'
    
    VALID_STATUSES = [STATUS_UNPAID, STATUS_PARTIAL, STATUS_PAID, STATUS_OVERDUE]
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    semester = db.Column(db.String(20), nullable=False)  # e.g., "2023/2024-Ganjil"
    total_amount = db.Column(db.Integer, nullable=False)  # Total SPP
    paid_amount = db.Column(db.Integer, default=0)  # Sudah dibayar
    remaining_amount = db.Column(db.Integer, nullable=False)  # Sisa pembayaran
    penalty = db.Column(db.Integer, default=0)  # Denda keterlambatan
    status = db.Column(db.String(20), default=STATUS_UNPAID)  # Status pembayaran
    due_date = db.Column(db.DateTime, nullable=False)
    last_payment_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='billing', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Billing {self.semester} - {self.status}>'
    
    @property
    def is_overdue(self):
        """Cek apakah tagihan sudah melampaui due date"""
        return datetime.utcnow() > self.due_date and self.status != self.STATUS_PAID
    
    @property
    def days_overdue(self):
        """Hitung berapa hari tagihan terlambat"""
        if not self.is_overdue:
            return 0
        return (datetime.utcnow() - self.due_date).days
    
    def calculate_penalty(self, penalty_per_day, max_penalty):
        """Hitung denda keterlambatan"""
        if not self.is_overdue:
            return 0
        
        days = self.days_overdue
        calculated_penalty = days * penalty_per_day
        
        # Jangan melebihi max penalty
        return min(calculated_penalty, max_penalty)
    
    def update_status(self):
        """Update status berdasarkan jumlah pembayaran"""
        if self.paid_amount == 0:
            self.status = self.STATUS_UNPAID
        elif self.paid_amount < self.total_amount:
            self.status = self.STATUS_PARTIAL
        else:
            self.status = self.STATUS_PAID
        
        # Cek jika overdue
        if self.is_overdue and self.status != self.STATUS_PAID:
            self.status = self.STATUS_OVERDUE


class Semester(db.Model):
    """Model untuk data semester"""
    __tablename__ = 'semesters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., "2023/2024-Ganjil"
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    billing_generation_date = db.Column(db.DateTime)  # Tanggal tagihan dibuat
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Semester {self.name}>'
