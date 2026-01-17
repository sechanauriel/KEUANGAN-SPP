#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script untuk menambahkan data mahasiswa"""

from app import create_app, db
from app.models.student import Student

app = create_app()

def add_students():
    """Tambahkan mahasiswa baru ke database"""
    with app.app_context():
        # Data mahasiswa yang akan ditambahkan
        students_data = [
            {
                'nim': '24360001',
                'name': 'MUHAMMAD SECHAN AURIEL',
                'email': 'sechanauriel@gmail.com',
                'phone': '085172225747',
                'program_studi_id': 1,  # Teknik Informatika
                'status': 'active'
            },
            {
                'nim': '24360002',
                'name': 'PUTRI NURHALIZA',
                'email': 'putrinurhaliza@gmail.com',
                'phone': '085771731588',
                'program_studi_id': 1,  # Teknik Informatika
                'status': 'active'
            },
        ]
        
        # Tambahkan setiap mahasiswa
        for data in students_data:
            existing = Student.query.filter_by(nim=data['nim']).first()
            if not existing:
                student = Student(**data)
                db.session.add(student)
                print(f"✅ Menambahkan: {data['name']}")
            else:
                print(f"⚠️  Sudah ada: {data['name']} ({data['nim']})")
        
        db.session.commit()
        
        # Tampilkan semua mahasiswa
        print("\n" + "="*60)
        print("📋 DAFTAR SEMUA MAHASISWA")
        print("="*60)
        students = Student.query.all()
        for i, s in enumerate(students, 1):
            prog = s.program_studi.name if s.program_studi else "Unknown"
            print(f"{i}. {s.nim} | {s.name:20} | {prog}")
        print("="*60)
        print(f"Total: {len(students)} mahasiswa")

if __name__ == '__main__':
    add_students()