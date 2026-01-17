# app/models/student.py
from app.models.base import db
from datetime import datetime

class Student(db.Model):
    """Model untuk data mahasiswa"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    program_studi_id = db.Column(db.Integer, db.ForeignKey('program_studi.id'), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, inactive, graduated
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    program_studi = db.relationship('ProgramStudi', backref='students')
    billings = db.relationship('Billing', backref='student', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.nim} - {self.name}>'
    
    def can_register_krs(self):
        """Cek apakah mahasiswa dapat mendaftar KRS (tidak ada tunggakan)"""
        # Import here to avoid circular dependency
        from app.models.billing import Billing
        unpaid_billings = Billing.query.filter(
            Billing.student_id == self.id,
            Billing.status.in_(['unpaid', 'partial', 'overdue'])
        ).first()
        return unpaid_billings is None
    
    def get_total_outstanding(self):
        """Hitung total tunggakan mahasiswa"""
        from sqlalchemy import func
        from app.models.billing import Billing
        outstanding = db.session.query(func.sum(Billing.remaining_amount)).filter(
            Billing.student_id == self.id,
            Billing.status.in_(['unpaid', 'partial', 'overdue'])
        ).scalar()
        return outstanding or 0


class ProgramStudi(db.Model):
    """Model untuk data program studi"""
    __tablename__ = 'program_studi'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    spp_amount = db.Column(db.Integer, nullable=False)  # Jumlah SPP per semester
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProgramStudi {self.name} - Rp {self.spp_amount:,}>'
