# app/routes/webhook_routes.py
from flask import Blueprint, request, jsonify
from app.services.payment_service import PaymentService
from app.utils.logger import logger
from app.config import Config
from app.models import db
from app.models.billing import Billing
from app.models.payment import Payment
from datetime import datetime
from uuid import uuid4

webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhook')
payment_service = PaymentService()

def _validate_webhook_payload(payload):
    """Validate webhook payload structure and required fields"""
    required_fields = ['transaction_id', 'amount', 'status', 'billing_id', 'student_id']
    
    errors = []
    for field in required_fields:
        if field not in payload:
            errors.append(f"Missing required field: {field}")
    
    # Validate amount
    if 'amount' in payload and payload['amount'] <= 0:
        errors.append("Amount must be greater than 0")
    
    # Validate status
    if 'status' in payload and payload['status'] not in ['success', 'pending', 'failed']:
        errors.append("Status must be one of: success, pending, failed")
    
    # Validate billing exists
    if 'billing_id' in payload:
        billing = Billing.query.get(payload['billing_id'])
        if not billing:
            errors.append(f"Billing ID {payload['billing_id']} not found")
    
    return errors

@webhook_bp.route('/payment', methods=['POST'])
def payment_webhook():
    """
    Handle payment webhook notification dari payment gateway
    
    POST /api/webhook/payment
    Required fields:
    - transaction_id: str (unique transaction identifier)
    - billing_id: int (billing ID yang dibayar)
    - student_id: int (student ID)
    - amount: float (jumlah pembayaran)
    - status: str (success, pending, failed)
    - payment_method: str (optional: credit_card, transfer, etc)
    - timestamp: str (optional: ISO format timestamp)
    
    Example:
    {
        "transaction_id": "TXN-2026-001",
        "billing_id": 1,
        "student_id": 1,
        "amount": 2500000,
        "status": "success",
        "payment_method": "transfer",
        "timestamp": "2026-01-17T17:30:00"
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        payload = request.get_json()
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate payload
        validation_errors = _validate_webhook_payload(payload)
        if validation_errors:
            logger.warning(f"Webhook validation failed: {validation_errors}")
            return jsonify({
                'success': False,
                'error': 'Validation failed',
                'details': validation_errors
            }), 400
        
        # Only process successful payments
        if payload['status'] != 'success':
            logger.info(f"Webhook received with status '{payload['status']}' - not processing")
            return jsonify({
                'success': True,
                'message': f"Webhook received with status '{payload['status']}' - acknowledged"
            }), 200
        
        # Handle webhook
        result = payment_service.handle_webhook(payload, Config.PAYMENT_GATEWAY_SECRET)
        
        # Return appropriate status code
        status_code = result.get('status_code', 200 if result['success'] else 400)
        
        response = {
            'success': result['success'],
            'message': result.get('message'),
            'payment_id': result.get('payment_id')
        }
        
        logger.info(f"Webhook processed successfully: {result['message']}")
        
        return jsonify(response), status_code
        
    except Exception as e:
        error_msg = f"Error processing webhook: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@webhook_bp.route('/test', methods=['POST'])
def test_webhook():
    """
    Test endpoint untuk webhook - untuk development/testing saja
    Echo back the payload yang dikirim
    
    POST /api/webhook/test
    {
        "any_data": "can be anything"
    }
    """
    try:
        # Hanya izinkan di development mode
        if not Config.DEBUG:
            return jsonify({
                'success': False,
                'error': 'Test webhook not available in production'
            }), 403
        
        # Echo back the payload
        payload = request.get_json()
        
        return jsonify({
            'success': True,
            'message': 'Webhook test successful',
            'received_payload': payload,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@webhook_bp.route('/health', methods=['GET'])
def webhook_health():
    """
    Health check endpoint untuk payment gateway
    
    GET /api/webhook/health
    """
    return jsonify({
        'status': 'healthy',
        'service': 'SPP Payment Webhook Handler',
        'timestamp': str(datetime.utcnow())
    }), 200

@webhook_bp.route('/simulate-payment', methods=['POST'])
def simulate_payment():
    """
    Simulate payment untuk testing (DEVELOPMENT ONLY)
    
    POST /api/webhook/simulate-payment
    {
        "billing_id": 1,
        "student_id": 1,
        "amount": 2500000,
        "payment_method": "transfer"
    }
    
    Ini akan send webhook ke /api/webhook/payment secara internal
    untuk simulate payment gateway notification
    """
    try:
        if not Config.DEBUG:
            return jsonify({
                'success': False,
                'error': 'Simulate payment only available in development mode'
            }), 403
        
        payload = request.get_json()
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400
        
        # Validate required fields
        required_fields = ['billing_id', 'student_id', 'amount']
        for field in required_fields:
            if field not in payload:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create webhook payload
        webhook_payload = {
            'transaction_id': f'SIM-{uuid4().hex[:12].upper()}',
            'reference_code': f'SIM-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
            'billing_id': payload['billing_id'],
            'student_id': payload['student_id'],
            'amount': payload['amount'],
            'status': 'success',
            'payment_method': payload.get('payment_method', 'simulated'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Process the simulated payment
        result = payment_service.handle_webhook(webhook_payload, Config.PAYMENT_GATEWAY_SECRET)
        
        return jsonify({
            'success': result['success'],
            'message': result.get('message'),
            'simulated_payload': webhook_payload,
            'payment_id': result.get('payment_id')
        }), (200 if result['success'] else 400)
        
    except Exception as e:
        error_msg = f"Error simulating payment: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@webhook_bp.route('/test-all-students', methods=['POST'])
def test_all_students():
    """
    Test payment untuk semua mahasiswa (DEVELOPMENT ONLY)
    Simulate pembayaran sebagian untuk semua pending billings
    
    POST /api/webhook/test-all-students
    {
        "amount_percentage": 50  (optional: 0-100, default 50)
    }
    """
    try:
        if not Config.DEBUG:
            return jsonify({
                'success': False,
                'error': 'Test endpoint only available in development mode'
            }), 403
        
        payload = request.get_json() if request.is_json else {}
        amount_percentage = payload.get('amount_percentage', 50)
        
        if not (0 < amount_percentage <= 100):
            return jsonify({
                'success': False,
                'error': 'amount_percentage must be between 1 and 100'
            }), 400
        
        # Get all pending billings
        pending_billings = Billing.query.filter(
            Billing.status.in_([Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL])
        ).all()
        
        if not pending_billings:
            return jsonify({
                'success': True,
                'message': 'No pending billings to process',
                'processed': 0
            }), 200
        
        results = []
        for billing in pending_billings:
            # Calculate payment amount
            payment_amount = int(billing.remaining_amount * (amount_percentage / 100))
            
            if payment_amount == 0:
                continue
            
            # Create simulated payment
            webhook_payload = {
                'transaction_id': f'TEST-{uuid4().hex[:12].upper()}',
                'reference_code': f'TEST-{billing.student_id}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
                'billing_id': billing.id,
                'student_id': billing.student_id,
                'amount': payment_amount,
                'status': 'success',
                'payment_method': 'test_transfer',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Process payment
            result = payment_service.handle_webhook(webhook_payload, Config.PAYMENT_GATEWAY_SECRET)
            
            results.append({
                'billing_id': billing.id,
                'student_id': billing.student_id,
                'amount_paid': payment_amount,
                'success': result['success']
            })
        
        return jsonify({
            'success': True,
            'message': f'Processed {len(results)} test payments',
            'processed': len(results),
            'results': results
        }), 200
        
    except Exception as e:
        error_msg = f"Error in test-all-students: {str(e)}"
        logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

