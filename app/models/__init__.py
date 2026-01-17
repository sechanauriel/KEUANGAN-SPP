# app/models/__init__.py
from .base import db
from .student import Student, ProgramStudi
from .billing import Billing
from .payment import Payment
from .payment_method import PaymentMethod

__all__ = [
    'db',
    'Student',
    'Billing',
    'Payment',
    'PaymentMethod',
    'ProgramStudi'
]
