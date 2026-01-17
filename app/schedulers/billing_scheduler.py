# app/schedulers/billing_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.billing_service import BillingService
from app.models import db
from app.models.billing import Semester, Billing
from app.models.student import Student
from app.utils.logger import logger
from datetime import datetime, timedelta
from app.config import Config

scheduler = BackgroundScheduler()
billing_service = BillingService()

def generate_billing_job():
    """
    Cron job untuk generate billing otomatis
    Dijalankan di awal semester
    """
    try:
        logger.info("Starting billing generation job...")
        
        # Ambil semester aktif
        active_semester = Semester.query.filter_by(is_active=True).first()
        
        if not active_semester:
            logger.warning("No active semester found")
            return
        
        # Cek apakah billing sudah di-generate untuk semester ini
        if active_semester.billing_generation_date:
            logger.info(f"Billing already generated for {active_semester.name}")
            return
        
        # Generate billing
        result = billing_service.generate_billing_for_semester(active_semester.id)
        
        if result['success']:
            # Update billing generation date
            active_semester.billing_generation_date = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Billing generation completed: {result['message']}")
        else:
            logger.error(f"Billing generation failed: {result['message']}")
            
    except Exception as e:
        logger.error(f"Error in billing generation job: {str(e)}")

def update_penalty_job():
    """
    Cron job untuk update denda keterlambatan
    Dijalankan setiap hari pada jam 00:00
    """
    try:
        logger.info("Starting penalty update job...")
        
        # Ambil semua billing yang belum dibayar
        unpaid_billings = Billing.query.filter(
            Billing.status.in_([Billing.STATUS_UNPAID, Billing.STATUS_PARTIAL, Billing.STATUS_OVERDUE])
        ).all()
        
        updated_count = 0
        for billing in unpaid_billings:
            penalty = billing.calculate_penalty(
                Config.OVERDUE_PENALTY_PER_DAY,
                Config.OVERDUE_MAX_PENALTY
            )
            
            if penalty != billing.penalty:
                billing.penalty = penalty
                
                # Update status to overdue if necessary
                if billing.is_overdue and billing.status != Billing.STATUS_PAID:
                    billing.status = Billing.STATUS_OVERDUE
                
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
            logger.info(f"Penalty update completed: {updated_count} billings updated")
        else:
            logger.info("No penalty updates needed")
            
    except Exception as e:
        logger.error(f"Error in penalty update job: {str(e)}")

def send_reminder_job():
    """
    Cron job untuk send reminder pembayaran
    Dijalankan setiap hari pukul 09:00
    """
    try:
        logger.info("Starting payment reminder job...")
        
        # Ambil billing yang akan jatuh tempo dalam 7 hari ke depan
        upcoming_due = Billing.query.filter(
            Billing.status != Billing.STATUS_PAID,
            Billing.due_date <= datetime.utcnow() + timedelta(days=7),
            Billing.due_date >= datetime.utcnow()
        ).all()
        
        # Ambil billing yang sudah overdue
        overdue_billings = Billing.query.filter(
            Billing.status == Billing.STATUS_OVERDUE
        ).all()
        
        all_reminders = upcoming_due + overdue_billings
        
        # TODO: Send email reminders
        # Implementasi email sending di sini
        
        logger.info(f"Reminder job completed: {len(all_reminders)} reminders to send")
        
    except Exception as e:
        logger.error(f"Error in reminder job: {str(e)}")

def setup_billing_scheduler(app):
    """
    Setup scheduler untuk billing tasks
    
    Args:
        app: Flask application instance
    """
    try:
        # Start scheduler
        if not scheduler.running:
            scheduler.start()
            logger.info("Scheduler started")
        
        # Add jobs
        # 1. Generate billing di awal semester (hari pertama setiap bulan)
        scheduler.add_job(
            func=generate_billing_job,
            trigger=CronTrigger(day=1, hour=0, minute=0),
            id='generate_billing_job',
            name='Generate Billing',
            replace_existing=True
        )
        
        # 2. Update penalty setiap hari (00:00)
        scheduler.add_job(
            func=update_penalty_job,
            trigger=CronTrigger(hour=0, minute=0),
            id='update_penalty_job',
            name='Update Penalty',
            replace_existing=True
        )
        
        # 3. Send reminder setiap hari (09:00)
        scheduler.add_job(
            func=send_reminder_job,
            trigger=CronTrigger(hour=9, minute=0),
            id='send_reminder_job',
            name='Send Payment Reminder',
            replace_existing=True
        )
        
        logger.info("Billing scheduler configured successfully")
        
    except Exception as e:
        logger.error(f"Error setting up scheduler: {str(e)}")

def shutdown_scheduler():
    """Shutdown scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shutdown")
