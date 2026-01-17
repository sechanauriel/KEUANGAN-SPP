# app/routes/student_routes.py
from flask import Blueprint, request, jsonify
from app.models.base import db
from app.models.student import Student, ProgramStudi
from app.utils.logger import logger
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/api/billing')

# ============================================================
# SPECIAL ROUTES - DEFINE BEFORE GENERIC ROUTES!
# ============================================================

@student_bp.route('/student/search', methods=['GET'])
def search_students():
    """
    Cari mahasiswa berdasarkan NIM atau nama
    
    GET /api/billing/student/search?q=nama_atau_nim
    """
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({'error': 'Query harus minimal 2 karakter'}), 400
        
        # Cari di NIM dan nama
        students = Student.query.filter(
            (Student.nim.ilike(f'%{query}%')) |
            (Student.name.ilike(f'%{query}%'))
        ).all()
        
        result = []
        for student in students:
            program = student.program_studi.name if student.program_studi else "Unknown"
            result.append({
                'id': student.id,
                'nim': student.nim,
                'name': student.name,
                'email': student.email,
                'program_studi': program,
                'status': student.status
            })
        
        return jsonify({
            'query': query,
            'total': len(result),
            'students': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching students: {str(e)}")
        return jsonify({'error': str(e)}), 500


@student_bp.route('/student/program/<int:program_id>', methods=['GET'])
def get_students_by_program(program_id):
    """
    Dapatkan mahasiswa berdasarkan program studi
    
    GET /api/billing/student/program/<program_id>
    """
    try:
        students = Student.query.filter_by(program_studi_id=program_id).all()
        program = ProgramStudi.query.get(program_id)
        
        if not program:
            return jsonify({'error': 'Program studi not found'}), 404
        
        result = []
        for student in students:
            result.append({
                'id': student.id,
                'nim': student.nim,
                'name': student.name,
                'email': student.email,
                'status': student.status
            })
        
        return jsonify({
            'program_studi': program.name,
            'total': len(result),
            'students': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching students by program: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ============================================================
# GENERIC ROUTES - DEFINE AFTER SPECIAL ROUTES
# ============================================================

@student_bp.route('/student', methods=['GET'])
def get_all_students():
    """
    Dapatkan daftar semua mahasiswa
    
    GET /api/billing/student
    """
    try:
        students = Student.query.all()
        result = []
        
        for student in students:
            program = student.program_studi.name if student.program_studi else "Unknown"
            result.append({
                'id': student.id,
                'nim': student.nim,
                'name': student.name,
                'email': student.email,
                'phone': student.phone,
                'program_studi': program,
                'status': student.status,
                'registration_date': student.registration_date.isoformat() if student.registration_date else None,
            })
        
        return jsonify({
            'total': len(result),
            'students': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}")
        return jsonify({'error': str(e)}), 500

@student_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    Dapatkan detail satu mahasiswa
    
    GET /api/billing/student/<student_id>
    """
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        program = student.program_studi.name if student.program_studi else "Unknown"
        
        return jsonify({
            'id': student.id,
            'nim': student.nim,
            'name': student.name,
            'email': student.email,
            'phone': student.phone,
            'program_studi': program,
            'program_studi_id': student.program_studi_id,
            'status': student.status,
            'registration_date': student.registration_date.isoformat() if student.registration_date else None,
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching student: {str(e)}")
        return jsonify({'error': str(e)}), 500

@student_bp.route('/student', methods=['POST'])
def create_student():
    """
    Tambah mahasiswa baru
    
    POST /api/billing/student
    
    Request Body:
    {
        "nim": "20241234",
        "name": "Nama Mahasiswa",
        "email": "email@email.com",
        "phone": "081234567890",
        "program_studi_id": 1,
        "status": "active"
    }
    """
    try:
        data = request.get_json()
        
        # Validasi required fields
        required_fields = ['nim', 'name', 'email', 'program_studi_id']
        missing = [f for f in required_fields if f not in data or not data[f]]
        
        if missing:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        # Cek apakah NIM sudah ada
        existing = Student.query.filter_by(nim=data['nim']).first()
        if existing:
            return jsonify({
                'error': f'NIM {data["nim"]} sudah terdaftar!'
            }), 409
        
        # Cek apakah program studi ada
        program = ProgramStudi.query.get(data['program_studi_id'])
        if not program:
            return jsonify({
                'error': f'Program studi dengan ID {data["program_studi_id"]} tidak ditemukan'
            }), 404
        
        # Buat mahasiswa baru
        student = Student(
            nim=data['nim'],
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            program_studi_id=data['program_studi_id'],
            status=data.get('status', 'active')
        )
        
        db.session.add(student)
        db.session.commit()
        
        logger.info(f"Student created: {student.nim} - {student.name}")
        
        return jsonify({
            'message': 'Student berhasil ditambahkan',
            'student': {
                'id': student.id,
                'nim': student.nim,
                'name': student.name,
                'email': student.email,
                'phone': student.phone,
                'program_studi': program.name,
                'status': student.status
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    Update data mahasiswa
    
    PUT /api/billing/student/<student_id>
    
    Request Body (semua optional):
    {
        "name": "Nama Baru",
        "email": "email_baru@email.com",
        "phone": "081234567890",
        "program_studi_id": 1,
        "status": "active"
    }
    """
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        data = request.get_json()
        
        # Update fields yang diberikan
        if 'name' in data:
            student.name = data['name']
        
        if 'email' in data:
            student.email = data['email']
        
        if 'phone' in data:
            student.phone = data['phone']
        
        if 'program_studi_id' in data:
            # Cek apakah program studi ada
            program = ProgramStudi.query.get(data['program_studi_id'])
            if not program:
                return jsonify({
                    'error': f'Program studi dengan ID {data["program_studi_id"]} tidak ditemukan'
                }), 404
            student.program_studi_id = data['program_studi_id']
        
        if 'status' in data:
            student.status = data['status']
        
        student.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Student updated: {student.nim} - {student.name}")
        
        program = student.program_studi.name if student.program_studi else "Unknown"
        
        return jsonify({
            'message': 'Student berhasil diupdate',
            'student': {
                'id': student.id,
                'nim': student.nim,
                'name': student.name,
                'email': student.email,
                'phone': student.phone,
                'program_studi': program,
                'status': student.status
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error updating student: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@student_bp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Hapus mahasiswa
    
    DELETE /api/billing/student/<student_id>
    """
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        nim = student.nim
        name = student.name
        
        db.session.delete(student)
        db.session.commit()
        
        logger.info(f"Student deleted: {nim} - {name}")
        
        return jsonify({
            'message': f'Mahasiswa {name} ({nim}) berhasil dihapus',
            'deleted_student': {
                'id': student_id,
                'nim': nim,
                'name': name
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


