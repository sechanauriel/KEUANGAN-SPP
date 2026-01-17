# app/routes/billing_routes.py
from flask import Blueprint, request, jsonify
from app.models.base import db
from app.services.billing_service import BillingService
from app.models.student import Student
from app.models.billing import Billing, Semester
from app.utils.logger import logger
from datetime import datetime

billing_bp = Blueprint('billing', __name__, url_prefix='/api/billing')
billing_service = BillingService()

@billing_bp.route('/semesters', methods=['GET'])
def get_semesters():
    """
    Dapatkan daftar semua semester (untuk dropdown selection)
    
    GET /api/billing/semesters
    
    Response:
    {
        "semesters": [
            {"id": 1, "name": "2026/2027-Ganjil", "is_active": true, "start_date": "...", "end_date": "..."},
            ...
        ]
    }
    """
    try:
        semesters = Semester.query.all()
        
        if not semesters:
            return jsonify({
                'semesters': [],
                'message': 'Belum ada semester. Silakan buat semester terlebih dahulu.'
            }), 200
        
        semesters_data = [
            {
                'id': s.id,
                'name': s.name,
                'is_active': s.is_active,
                'start_date': s.start_date.isoformat() if s.start_date else None,
                'end_date': s.end_date.isoformat() if s.end_date else None,
                'billing_generation_date': s.billing_generation_date.isoformat() if s.billing_generation_date else None
            }
            for s in semesters
        ]
        
        return jsonify({'semesters': semesters_data}), 200
        
    except Exception as e:
        error_msg = f"Error fetching semesters: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@billing_bp.route('/generate/<int:semester_id>', methods=['POST'])
def generate_billing(semester_id):
    """
    Generate billing untuk semester tertentu
    
    POST /api/billing/generate/<semester_id>
    """
    try:
        due_days = request.json.get('due_days', 14) if request.json else 14
        
        # Validate semester exists
        semester = Semester.query.get(semester_id)
        if not semester:
            available_semesters = Semester.query.all()
            available_ids = [s.id for s in available_semesters]
            
            if available_semesters:
                return jsonify({
                    'success': False,
                    'message': f'Semester dengan ID {semester_id} tidak ditemukan',
                    'available_semesters': [
                        {'id': s.id, 'name': s.name, 'is_active': s.is_active}
                        for s in available_semesters
                    ],
                    'hint': f'Semester yang tersedia: {available_ids}'
                }), 404
            else:
                return jsonify({
                    'success': False,
                    'message': f'Semester dengan ID {semester_id} tidak ditemukan',
                    'available_semesters': [],
                    'hint': 'Belum ada semester di database. Gunakan setup_semester.py atau buat semester di dashboard.'
                }), 404
        
        result = billing_service.generate_billing_for_semester(semester_id, due_days)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        error_msg = f"Error generating billing: {str(e)}"
        logger.error(error_msg)
        return jsonify({'success': False, 'message': error_msg}), 500

@billing_bp.route('/student/<int:student_id>', methods=['GET'])
def get_student_billing(student_id):
    """
    Dapatkan billing details untuk satu mahasiswa
    
    GET /api/billing/student/<student_id>
    """
    try:
        summary = billing_service.get_billing_summary(student_id)
        
        if 'error' in summary:
            return jsonify(summary), 404
        
        # Format response
        response = {
            'student': {
                'id': summary['student'].id,
                'nim': summary['student'].nim,
                'name': summary['student'].name,
                'program_studi': summary['student'].program_studi.name
            },
            'summary': {
                'total_billed': summary['total_billed'],
                'total_paid': summary['total_paid'],
                'total_outstanding': summary['total_outstanding'],
                'payment_percentage': (summary['total_paid'] / summary['total_billed'] * 100) if summary['total_billed'] > 0 else 0
            },
            'billings': [
                {
                    'id': b.id,
                    'semester': b.semester,
                    'total_amount': b.total_amount,
                    'paid_amount': b.paid_amount,
                    'remaining_amount': b.remaining_amount,
                    'penalty': b.penalty,
                    'status': b.status,
                    'due_date': b.due_date.isoformat(),
                    'is_overdue': b.is_overdue,
                    'days_overdue': b.days_overdue if b.is_overdue else 0
                }
                for b in summary['billings']
            ]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = f"Error fetching billing: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@billing_bp.route('/can-register/<int:student_id>', methods=['GET'])
def can_register_krs(student_id):
    """
    Cek apakah mahasiswa bisa mendaftar KRS (tidak ada tunggakan)
    
    GET /api/billing/can-register/<student_id>
    """
    try:
        result = billing_service.can_student_register_krs(student_id)
        
        status_code = 200 if result['can_register'] else 403
        return jsonify(result), status_code
        
    except Exception as e:
        error_msg = f"Error checking KRS eligibility: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@billing_bp.route('/update-penalty/<int:billing_id>', methods=['POST'])
def update_penalty(billing_id):
    """
    Update denda keterlambatan untuk satu billing
    
    POST /api/billing/update-penalty/<billing_id>
    """
    try:
        from app.config import Config
        
        result = billing_service.calculate_and_update_penalty(
            billing_id,
            Config.OVERDUE_PENALTY_PER_DAY,
            Config.OVERDUE_MAX_PENALTY
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify({
            'success': True,
            'message': 'Penalty updated',
            'penalty': result['penalty'],
            'billing': {
                'id': result['billing'].id,
                'status': result['billing'].status
            }
        }), 200
        
    except Exception as e:
        error_msg = f"Error updating penalty: {str(e)}"
        logger.error(error_msg)
        return jsonify({'success': False, 'message': error_msg}), 500

@billing_bp.route('/outstanding', methods=['GET'])
def get_outstanding_billings():
    """
    Dapatkan daftar billing yang outstanding (belum dibayar/partial/overdue)
    
    GET /api/billing/outstanding?limit=20&offset=0&status=overdue
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        status_filter = request.args.get('status')  # unpaid, partial, overdue
        
        query = Billing.query.filter(
            Billing.status != Billing.STATUS_PAID
        )
        
        if status_filter and status_filter in Billing.VALID_STATUSES:
            query = query.filter_by(status=status_filter)
        
        total = query.count()
        billings = query.order_by(Billing.created_at.desc()).limit(limit).offset(offset).all()
        
        response = {
            'total': total,
            'limit': limit,
            'offset': offset,
            'billings': [
                {
                    'id': b.id,
                    'student': {
                        'nim': b.student.nim,
                        'name': b.student.name
                    },
                    'semester': b.semester,
                    'total_amount': b.total_amount,
                    'remaining_amount': b.remaining_amount,
                    'penalty': b.penalty,
                    'status': b.status,
                    'due_date': b.due_date.isoformat(),
                    'days_overdue': b.days_overdue if b.is_overdue else 0
                }
                for b in billings
            ]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = f"Error fetching outstanding billings: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@billing_bp.route('/krs-eligibility-report', methods=['GET'])
def get_krs_eligibility_report():
    """
    Dapatkan laporan eligibility KRS untuk semua mahasiswa (real-time)
    
    GET /api/billing/krs-eligibility-report?eligible=all
    
    Query parameters:
    - eligible: all, eligible, not_eligible (default: all)
    - limit: max rows (default: 100)
    - offset: pagination (default: 0)
    
    Response:
    {
        "timestamp": "2026-01-17T...",
        "summary": {
            "total_students": 3,
            "eligible_for_krs": 1,
            "blocked_from_krs": 2,
            "total_blocked_arrears": 10000000
        },
        "students": [
            {
                "student_id": 1,
                "nim": "2023001",
                "name": "John Doe",
                "program_studi": "Teknik Informatika",
                "eligible_for_krs": true,
                "outstanding": 0
            },
            {
                "student_id": 2,
                "nim": "2023002",
                "name": "Jane Smith",
                "program_studi": "Teknik Informatika",
                "eligible_for_krs": false,
                "outstanding": 5000000,
                "reason": "Has unpaid billing"
            },
            ...
        ]
    }
    """
    try:
        from app.models.student import Student
        from app.models.billing import Billing
        from sqlalchemy import func
        
        filter_param = request.args.get('eligible', 'all').lower()
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Validate filter
        if filter_param not in ['all', 'eligible', 'not_eligible']:
            return jsonify({
                'error': 'Invalid eligible parameter. Must be: all, eligible, or not_eligible'
            }), 400
        
        # Get all active students
        all_students = Student.query.filter_by(status='active').all()
        
        eligible_count = 0
        not_eligible_count = 0
        total_arrears = 0
        
        students_data = []
        
        for student in all_students:
            # Calculate outstanding
            outstanding_billings = Billing.query.filter(
                Billing.student_id == student.id,
                Billing.status.in_([Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL, Billing.STATUS_OVERDUE])
            ).all()
            
            total_outstanding = sum(b.remaining_amount for b in outstanding_billings)
            is_eligible = total_outstanding == 0
            
            if is_eligible:
                eligible_count += 1
            else:
                not_eligible_count += 1
                total_arrears += total_outstanding
            
            # Apply filter
            if filter_param == 'eligible' and not is_eligible:
                continue
            if filter_param == 'not_eligible' and is_eligible:
                continue
            
            student_info = {
                'student_id': student.id,
                'nim': student.nim,
                'name': student.name,
                'program_studi': student.program_studi.name if student.program_studi else None,
                'eligible_for_krs': is_eligible,
                'outstanding': total_outstanding
            }
            
            if not is_eligible:
                student_info['reason'] = 'Has unpaid billing' if total_outstanding > 0 else 'Unknown'
            
            students_data.append(student_info)
        
        # Apply pagination
        total_filtered = len(students_data)
        students_data = students_data[offset:offset + limit]
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'filter': filter_param,
            'summary': {
                'total_students': len(all_students),
                'eligible_for_krs': eligible_count,
                'blocked_from_krs': not_eligible_count,
                'total_blocked_arrears': total_arrears
            },
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total': total_filtered
            },
            'students': students_data
        }), 200
        
    except Exception as e:
        error_msg = f"Error generating KRS eligibility report: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@billing_bp.route('/<int:billing_id>', methods=['DELETE'])
def delete_billing(billing_id):
    """
    Hapus/Delete billing tertentu
    
    DELETE /api/billing/<billing_id>
    
    Response:
    {
        "success": true,
        "message": "Billing berhasil dihapus",
        "deleted_billing": {
            "id": 1,
            "student_id": 1,
            "total_amount": 5000000,
            "status": "unpaid"
        }
    }
    """
    try:
        billing = Billing.query.get(billing_id)
        
        if not billing:
            return jsonify({
                'success': False,
                'message': f'Billing dengan ID {billing_id} tidak ditemukan'
            }), 404
        
        # Store data sebelum delete untuk response
        deleted_data = {
            'id': billing.id,
            'student_id': billing.student_id,
            'semester': billing.semester,
            'total_amount': billing.total_amount,
            'paid_amount': billing.paid_amount,
            'remaining_amount': billing.remaining_amount,
            'status': billing.status,
            'created_at': billing.created_at.isoformat() if billing.created_at else None
        }
        
        # Delete
        db.session.delete(billing)
        db.session.commit()
        
        logger.info(f"Billing {billing_id} deleted successfully")
        
        return jsonify({
            'success': True,
            'message': f'Billing dengan ID {billing_id} berhasil dihapus',
            'deleted_billing': deleted_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"Error deleting billing: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'message': error_msg
        }), 500

@billing_bp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student_billings(student_id):
    """
    Hapus semua billing untuk satu mahasiswa
    
    DELETE /api/billing/student/<student_id>
    
    Response:
    {
        "success": true,
        "message": "Semua billing untuk mahasiswa berhasil dihapus",
        "deleted_count": 2
    }
    """
    try:
        student = Student.query.get(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'message': f'Mahasiswa dengan ID {student_id} tidak ditemukan'
            }), 404
        
        # Get all billings for this student
        billings = Billing.query.filter_by(student_id=student_id).all()
        deleted_count = len(billings)
        
        if deleted_count == 0:
            return jsonify({
                'success': True,
                'message': f'Tidak ada billing untuk mahasiswa ID {student_id}',
                'deleted_count': 0
            }), 200
        
        # Delete all billings
        for billing in billings:
            db.session.delete(billing)
        
        db.session.commit()
        
        logger.info(f"Deleted {deleted_count} billings for student {student_id}")
        
        return jsonify({
            'success': True,
            'message': f'Semua billing untuk mahasiswa {student.name} ({student.nim}) berhasil dihapus',
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"Error deleting student billings: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'message': error_msg
        }), 500

@billing_bp.route('/semester/<int:semester_id>', methods=['DELETE'])
def delete_semester_billings(semester_id):
    """
    Hapus semua billing untuk satu semester
    
    DELETE /api/billing/semester/<semester_id>
    
    Response:
    {
        "success": true,
        "message": "Semua billing untuk semester berhasil dihapus",
        "deleted_count": 50
    }
    """
    try:
        semester = Semester.query.get(semester_id)
        
        if not semester:
            return jsonify({
                'success': False,
                'message': f'Semester dengan ID {semester_id} tidak ditemukan'
            }), 404
        
        # Get all billings for this semester
        billings = Billing.query.filter(
            Billing.student_id.in_(
                db.session.query(Student.id).all()
            ),
            Billing.semester == semester.name
        ).all()
        
        deleted_count = len(billings)
        
        if deleted_count == 0:
            return jsonify({
                'success': True,
                'message': f'Tidak ada billing untuk semester ID {semester_id}',
                'deleted_count': 0
            }), 200
        
        # Delete all billings
        for billing in billings:
            db.session.delete(billing)
        
        db.session.commit()
        
        # Reset billing generation date
        semester.billing_generation_date = None
        db.session.commit()
        
        logger.info(f"Deleted {deleted_count} billings for semester {semester_id}")
        
        return jsonify({
            'success': True,
            'message': f'Semua billing untuk semester {semester.name} berhasil dihapus',
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"Error deleting semester billings: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'message': error_msg
        }), 500

