# app/routes/dashboard_routes.py
from flask import Blueprint, request, jsonify
from app.services.ai_service import AIFinancialService
from app.utils.logger import logger
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
ai_service = AIFinancialService()

@dashboard_bp.route('/financial-report', methods=['GET'])
def get_financial_report():
    """
    Dapatkan laporan keuangan dengan AI insights
    
    GET /api/dashboard/financial-report?days=30
    """
    try:
        days = request.args.get('days', 30, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        end_date = datetime.utcnow()
        
        report = ai_service.generate_financial_report(start_date, end_date)
        
        return jsonify(report), 200
        
    except Exception as e:
        error_msg = f"Error generating financial report: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@dashboard_bp.route('/student-profile/<int:student_id>', methods=['GET'])
def get_student_profile(student_id):
    """
    Dapatkan profil finansial lengkap untuk satu mahasiswa
    
    GET /api/dashboard/student-profile/<student_id>
    """
    try:
        profile = ai_service.get_student_financial_profile(student_id)
        
        if 'error' in profile:
            return jsonify(profile), 404
        
        return jsonify(profile), 200
        
    except Exception as e:
        error_msg = f"Error fetching student profile: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@dashboard_bp.route('/summary', methods=['GET'])
def get_dashboard_summary():
    """
    Dapatkan ringkasan dashboard (quick stats)
    
    GET /api/dashboard/summary
    """
    try:
        from app.models import db
        from app.models.billing import Billing
        from app.models.student import Student
        from app.models.payment import Payment
        from sqlalchemy import func
        
        # Calculate metrics
        total_students = Student.query.filter_by(status='active').count()
        
        total_billed_query = db.session.query(func.sum(Billing.total_amount)).filter(
            Billing.status != Billing.STATUS_PAID
        ).scalar()
        total_billed = total_billed_query or 0
        
        total_outstanding_query = db.session.query(func.sum(Billing.remaining_amount)).filter(
            Billing.status.in_([Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL, Billing.STATUS_OVERDUE])
        ).scalar()
        total_outstanding = total_outstanding_query or 0
        
        total_paid_query = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == Payment.STATUS_CONFIRMED
        ).scalar()
        total_paid = total_paid_query or 0
        
        num_overdue = Billing.query.filter_by(status=Billing.STATUS_OVERDUE).count()
        
        collection_rate = (total_paid / total_billed * 100) if total_billed > 0 else 0
        
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': {
                'total_active_students': total_students,
                'total_billed': total_billed,
                'total_paid': total_paid,
                'total_outstanding': total_outstanding,
                'collection_rate': round(collection_rate, 2),
                'students_with_overdue': num_overdue
            }
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        error_msg = f"Error generating dashboard summary: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@dashboard_bp.route('/program-studi-stats', methods=['GET'])
def get_program_studi_statistics():
    """
    Dapatkan statistik per program studi
    
    GET /api/dashboard/program-studi-stats
    """
    try:
        from app.models import db
        from app.models.student import ProgramStudi
        from app.models.student import Student
        from app.models.billing import Billing
        from app.models.payment import Payment
        from sqlalchemy import func
        
        program_studi_list = ProgramStudi.query.all()
        
        stats = []
        for program in program_studi_list:
            students = Student.query.filter_by(program_studi_id=program.id, status='active').count()
            
            billings_total = db.session.query(func.sum(Billing.total_amount)).filter(
                Billing.student_id.in_(
                    db.session.query(Student.id).filter_by(program_studi_id=program.id)
                )
            ).scalar() or 0
            
            paid_total = db.session.query(func.sum(Payment.amount)).filter(
                Payment.student_id.in_(
                    db.session.query(Student.id).filter_by(program_studi_id=program.id)
                ),
                Payment.status == Payment.STATUS_CONFIRMED
            ).scalar() or 0
            
            collection_rate = (paid_total / billings_total * 100) if billings_total > 0 else 0
            
            stats.append({
                'program_studi': program.name,
                'num_students': students,
                'total_billed': billings_total,
                'total_paid': paid_total,
                'collection_rate': round(collection_rate, 2)
            })
        
        return jsonify({
            'program_studi_statistics': stats
        }), 200
        
    except Exception as e:
        error_msg = f"Error generating program studi statistics: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@dashboard_bp.route('/billing-breakdown', methods=['GET'])
def get_billing_breakdown():
    """
    Dapatkan breakdown billing berdasarkan status (real-time)
    
    GET /api/dashboard/billing-breakdown
    
    Response:
    {
        "timestamp": "2026-01-17T...",
        "breakdown": {
            "unpaid": {"count": 5, "total": 25000000},
            "partial": {"count": 2, "total": 10000000},
            "paid": {"count": 10, "total": 50000000},
            "overdue": {"count": 1, "total": 5000000}
        }
    }
    """
    try:
        from app.models import db
        from app.models.billing import Billing
        from sqlalchemy import func
        
        statuses = [Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL, Billing.STATUS_PAID, Billing.STATUS_OVERDUE]
        
        breakdown = {}
        for status in statuses:
            count = Billing.query.filter_by(status=status).count()
            total = db.session.query(func.sum(Billing.total_amount)).filter_by(status=status).scalar() or 0
            
            breakdown[status.lower()] = {
                'count': count,
                'total': total
            }
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'breakdown': breakdown
        }), 200
        
    except Exception as e:
        error_msg = f"Error generating billing breakdown: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@dashboard_bp.route('/students-status', methods=['GET'])
def get_students_payment_status():
    """
    Dapatkan status pembayaran semua mahasiswa (real-time)
    
    GET /api/dashboard/students-status?status=unpaid
    
    Query parameters:
    - status: unpaid, partial, paid, overdue, all (default: all)
    - limit: max rows (default: 100)
    - offset: pagination (default: 0)
    
    Response:
    {
        "timestamp": "2026-01-17T...",
        "students": [
            {
                "student_id": 1,
                "nim": "2023001",
                "name": "John Doe",
                "program_studi": "Teknik Informatika",
                "total_outstanding": 4000000,
                "latest_billing_status": "unpaid",
                "can_register_krs": false
            },
            ...
        ]
    }
    """
    try:
        from app.models import db
        from app.models.student import Student
        from app.models.billing import Billing
        
        status_filter = request.args.get('status', 'all').lower()
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Get active students
        query = Student.query.filter_by(status='active')
        
        # Apply status filter if specified
        if status_filter != 'all':
            valid_statuses = ['unpaid', 'partial', 'paid', 'overdue']
            if status_filter not in valid_statuses:
                return jsonify({
                    'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
                }), 400
            
            # Get students with specific billing status
            students_with_status = db.session.query(Student.id).join(Billing).filter(
                Billing.status == status_filter.upper()
            ).distinct()
            query = query.filter(Student.id.in_(students_with_status))
        
        total_students = query.count()
        students = query.offset(offset).limit(limit).all()
        
        students_data = []
        for student in students:
            # Calculate total outstanding
            outstanding_billings = Billing.query.filter(
                Billing.student_id == student.id,
                Billing.status.in_([Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL, Billing.STATUS_OVERDUE])
            ).all()
            
            total_outstanding = sum(b.remaining_amount for b in outstanding_billings)
            
            # Get latest billing status
            latest_billing = Billing.query.filter_by(student_id=student.id).order_by(
                Billing.created_at.desc()
            ).first()
            
            students_data.append({
                'student_id': student.id,
                'nim': student.nim,
                'name': student.name,
                'program_studi': student.program_studi.name if student.program_studi else None,
                'total_outstanding': total_outstanding,
                'latest_billing_status': latest_billing.status if latest_billing else None,
                'can_register_krs': total_outstanding == 0
            })
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'filter': status_filter,
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total': total_students
            },
            'students': students_data
        }), 200
        
    except Exception as e:
        error_msg = f"Error fetching students payment status: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@dashboard_bp.route('/daily-report', methods=['GET'])
def get_daily_report():
    """
    Dapatkan laporan harian (real-time)
    
    GET /api/dashboard/daily-report
    
    Response:
    {
        "timestamp": "2026-01-17T...",
        "report_date": "2026-01-17",
        "summary": {
            "payments_received_today": 5000000,
            "payments_count": 2,
            "new_billings": 0,
            "overdue_count": 1
        },
        "trends": {
            "collection_rate": 33.33,
            "average_payment": 2500000
        }
    }
    """
    try:
        from app.models import db
        from app.models.billing import Billing
        from app.models.payment import Payment
        from sqlalchemy import func
        
        today = datetime.utcnow().date()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())
        
        # Payments received today
        payments_today_total = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == Payment.STATUS_CONFIRMED,
            Payment.created_at.between(today_start, today_end)
        ).scalar() or 0
        
        payments_today_count = Payment.query.filter(
            Payment.status == Payment.STATUS_CONFIRMED,
            Payment.created_at.between(today_start, today_end)
        ).count()
        
        # New billings today
        new_billings = Billing.query.filter(
            Billing.created_at.between(today_start, today_end)
        ).count()
        
        # Overdue count
        overdue_count = Billing.query.filter(
            Billing.status == Billing.STATUS_OVERDUE
        ).count()
        
        # Collection rate
        total_billed = db.session.query(func.sum(Billing.total_amount)).scalar() or 0
        total_paid = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == Payment.STATUS_CONFIRMED
        ).scalar() or 0
        collection_rate = (total_paid / total_billed * 100) if total_billed > 0 else 0
        
        # Average payment
        average_payment = (payments_today_total / payments_today_count) if payments_today_count > 0 else 0
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'report_date': str(today),
            'summary': {
                'payments_received_today': payments_today_total,
                'payments_count': payments_today_count,
                'new_billings': new_billings,
                'overdue_count': overdue_count
            },
            'trends': {
                'collection_rate': round(collection_rate, 2),
                'average_payment': round(average_payment, 0)
            }
        }), 200
        
    except Exception as e:
        error_msg = f"Error generating daily report: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

