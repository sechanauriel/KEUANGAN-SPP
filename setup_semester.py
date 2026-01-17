#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script untuk membuat Semester dan data test
"""

from app import create_app, db
from app.models.billing import Semester
from app.models.student import Student, ProgramStudi
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("=" * 60)
    print("SETUP SEMESTER & DATA TEST")
    print("=" * 60)
    
    # 1. Check students
    print("\n1️⃣ Checking Students...")
    students = Student.query.all()
    print(f"   Total students: {len(students)}")
    if students:
        for s in students:
            print(f"   - {s.nim}: {s.name} ({s.program_studi.name if s.program_studi else 'N/A'})")
    else:
        print("   ⚠️  No students found!")
    
    # 2. Check Program Studi
    print("\n2️⃣ Checking Program Studi...")
    programs = ProgramStudi.query.all()
    print(f"   Total programs: {len(programs)}")
    for p in programs:
        print(f"   - {p.name} (SPP: Rp {p.spp_amount:,})")
    
    # 3. Check Semesters
    print("\n3️⃣ Checking Semesters...")
    semesters = Semester.query.all()
    print(f"   Total semesters: {len(semesters)}")
    if semesters:
        for s in semesters:
            status = "🟢 ACTIVE" if s.is_active else "⚫ INACTIVE"
            print(f"   - ID {s.id}: {s.name} {status}")
    else:
        print("   ⚠️  No semesters found! Creating new semester...")
        semester = Semester(
            name='2026/2027-Ganjil',
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=120),
            is_active=True
        )
        db.session.add(semester)
        db.session.commit()
        print(f"   ✅ Semester created: ID {semester.id} - {semester.name}")
    
    # 4. Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Students: {len(students)}")
    print(f"  Programs: {len(programs)}")
    print(f"  Semesters: {len(Semester.query.all())}")
    
    if len(students) > 0 and len(Semester.query.all()) > 0:
        sem_id = Semester.query.first().id
        print(f"\n✅ Ready to generate billing!")
        print(f"   Use Semester ID: {sem_id}")
    else:
        print("\n❌ Missing data! Need:")
        if len(students) == 0:
            print("   - Students (run: python add_students.py)")
        if len(Semester.query.all()) == 0:
            print("   - Semesters (created above)")
    
    print("=" * 60)
