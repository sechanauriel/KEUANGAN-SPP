#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPP Management System - Payment Management Application
Module: MINGGU 11 - Sistem Manajemen Keuangan SPP

Sistem ini menyediakan:
1. Payment Schema dengan status tracking (unpaid, partial, paid, overdue)
2. Billing Service untuk generate tagihan, process pembayaran, dan calculate denda
3. Dashboard Keuangan untuk menampilkan data per mahasiswa dan per program studi
4. Payment Webhook untuk menerima notifikasi dari payment gateway
5. AI Financial Report untuk generate insight dan rekomendasi
"""

import os
from flask import render_template
from datetime import datetime
from app import create_app, db
from app.models.student import Student, ProgramStudi
from app.models.billing import Billing, Semester
from app.models.payment import Payment, PaymentReconciliation
from app.models.payment_method import PaymentMethod

# Create Flask app
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    """Register models and db untuk Flask shell"""
    return {
        'db': db,
        'Student': Student,
        'ProgramStudi': ProgramStudi,
        'Billing': Billing,
        'Semester': Semester,
        'Payment': Payment,
        'PaymentMethod': PaymentMethod,
        'PaymentReconciliation': PaymentReconciliation
    }

@app.route('/')
def index():
    """Render Dashboard HTML"""
    return render_template('index.html')

@app.route('/student')
def student_management():
    """Render Student Management HTML"""
    return render_template('student_management.html')

@app.route('/api')
def api_home():
    """API home endpoint"""
    return {
        'message': 'SPP Management System API',
        'version': '1.0.0',
        'module': 'MINGGU 11 - Modul Keuangan (SPP)',
        'endpoints': {
            'student': '/api/student',
            'billing': '/api/billing',
            'payment': '/api/payment',
            'webhook': '/api/webhook',
            'dashboard': '/api/dashboard'
        },
        'documentation': 'Visit http://localhost:5000 for main dashboard',
        'student_management': 'Visit http://localhost:5000/student for student management'
    }, 200

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'SPP Management System',
        'timestamp': str(datetime.utcnow())
    }, 200

if __name__ == '__main__':
    from datetime import datetime
    
    print("""
    ╔════════════════════════════════════════════════════════════════════════╗
    ║   SPP MANAGEMENT SYSTEM - MINGGU 11: Modul Keuangan                   ║
    ║   Payment Management with AI Financial Reporting                       ║
    ╚════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize sample data
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if sample data exists
        if ProgramStudi.query.count() == 0:
            print("➕ Creating sample program studi...")
            program_studi_data = [
                ProgramStudi(name='Teknik Informatika', code='TI', spp_amount=5000000),
                ProgramStudi(name='Ekonomi', code='EK', spp_amount=4000000),
                ProgramStudi(name='Hukum', code='HK', spp_amount=3500000),
                ProgramStudi(name='Teknik Sipil', code='TS', spp_amount=5500000),
            ]
            for ps in program_studi_data:
                db.session.add(ps)
            db.session.commit()
            print("✅ Sample program studi created")
        
        if PaymentMethod.query.count() == 0:
            print("➕ Creating sample payment methods...")
            payment_methods = [
                PaymentMethod(
                    name='BCA Transfer',
                    method_type=PaymentMethod.METHOD_BANK_TRANSFER,
                    provider='BCA',
                    gateway_code='bca_transfer',
                    description='Pembayaran via transfer BCA'
                ),
                PaymentMethod(
                    name='BCA Virtual Account',
                    method_type=PaymentMethod.METHOD_VIRTUAL_ACCOUNT,
                    provider='BCA',
                    gateway_code='bca_virtual',
                    description='Pembayaran via Virtual Account BCA'
                ),
                PaymentMethod(
                    name='GCash',
                    method_type=PaymentMethod.METHOD_E_WALLET,
                    provider='GCash',
                    gateway_code='gcash',
                    description='Pembayaran via GCash'
                ),
                PaymentMethod(
                    name='Credit Card',
                    method_type=PaymentMethod.METHOD_CREDIT_CARD,
                    provider='Midtrans',
                    gateway_code='credit_card',
                    description='Pembayaran via Kartu Kredit'
                ),
            ]
            for pm in payment_methods:
                db.session.add(pm)
            db.session.commit()
            print("✅ Sample payment methods created")
        
        print(f"✅ Database initialized at: spp_management.db")
    
    print("\n📚 API Documentation:")
    print("   - Billing APIs: http://localhost:5000/api/billing")
    print("   - Payment APIs: http://localhost:5000/api/payment")
    print("   - Webhook APIs: http://localhost:5000/api/webhook")
    print("   - Dashboard APIs: http://localhost:5000/api/dashboard")
    print("\n▶️  Starting Flask development server...")
    print("   Server running at: http://localhost:5000")
    print("   Press CTRL+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
