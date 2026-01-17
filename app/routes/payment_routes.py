# app/routes/payment_routes.py
from flask import Blueprint, request, jsonify
from app.services.payment_service import PaymentService
from app.models.payment import Payment
from app.utils.logger import logger
from datetime import datetime, timedelta

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payment')
payment_service = PaymentService()

@payment_bp.route('/process', methods=['POST'])
def process_payment():
    """
    Process pembayaran manual
    
    POST /api/payment/process
    {
        "billing_id": 1,
        "amount": 5000000,
        "payment_method_id": 1,
        "transaction_id": "TXN123456",
        "gateway_name": "manual"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        required_fields = ['billing_id', 'amount', 'payment_method_id', 'transaction_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
        
        result = payment_service.process_payment(
            billing_id=data['billing_id'],
            amount=data['amount'],
            payment_method_id=data['payment_method_id'],
            transaction_id=data['transaction_id'],
            gateway_name=data.get('gateway_name', 'manual')
        )
        
        status_code = 201 if result['success'] else 400
        
        response = {
            'success': result['success'],
            'message': result.get('message'),
            'payment': {
                'id': result['payment'].id,
                'reference_code': result['payment'].reference_code,
                'amount': result['payment'].amount,
                'status': result['payment'].status
            } if 'payment' in result else None,
            'billing': {
                'id': result['billing'].id,
                'status': result['billing'].status,
                'remaining_amount': result['billing'].remaining_amount
            } if 'billing' in result else None
        }
        
        return jsonify(response), status_code
        
    except Exception as e:
        error_msg = f"Error processing payment: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@payment_bp.route('/history/<int:student_id>', methods=['GET'])
def get_payment_history(student_id):
    """
    Dapatkan riwayat pembayaran untuk satu mahasiswa
    
    GET /api/payment/history/<student_id>?limit=10
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        
        payments = payment_service.get_payment_history(student_id, limit)
        
        response = {
            'total': len(payments),
            'payments': [
                {
                    'id': p.id,
                    'reference_code': p.reference_code,
                    'amount': p.amount,
                    'status': p.status,
                    'payment_date': p.payment_date.isoformat() if p.payment_date else None,
                    'confirmation_date': p.confirmation_date.isoformat() if p.confirmation_date else None,
                    'payment_method': p.payment_method.name,
                    'gateway': p.gateway_name
                }
                for p in payments
            ]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = f"Error fetching payment history: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@payment_bp.route('/statistics', methods=['GET'])
def get_payment_statistics():
    """
    Dapatkan statistik pembayaran
    
    GET /api/payment/statistics?days=30
    """
    try:
        days = request.args.get('days', 30, type=int)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        end_date = datetime.utcnow()
        
        stats = payment_service.get_payment_statistics(start_date, end_date)
        
        response = {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': days
            },
            'statistics': {
                'total_payments': stats['total_payments'],
                'total_amount': stats['total_amount'],
                'average_amount': round(stats['average_amount'], 2),
                'daily_average': round(stats['total_amount'] / days, 2) if days > 0 else 0
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = f"Error fetching payment statistics: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment_detail(payment_id):
    """
    Dapatkan detail pembayaran
    
    GET /api/payment/<payment_id>
    """
    try:
        payment = Payment.query.get(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        response = {
            'payment': {
                'id': payment.id,
                'reference_code': payment.reference_code,
                'transaction_id': payment.transaction_id,
                'amount': payment.amount,
                'status': payment.status,
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None,
                'confirmation_date': payment.confirmation_date.isoformat() if payment.confirmation_date else None,
                'payment_method': payment.payment_method.name,
                'gateway': payment.gateway_name,
                'notes': payment.notes
            },
            'student': {
                'id': payment.student.id,
                'nim': payment.student.nim,
                'name': payment.student.name
            },
            'billing': {
                'id': payment.billing.id,
                'semester': payment.billing.semester,
                'status': payment.billing.status
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        error_msg = f"Error fetching payment detail: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': error_msg}), 500
