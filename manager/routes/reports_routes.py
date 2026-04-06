from manager.services.reports_service import ReportsService
from flask import Blueprint, request as rq, jsonify

reports_bp = Blueprint("Dashboards", __name__)
reports_service = ReportsService()

@reports_bp.route("")
def main(): return reports_service.get_reports_welcome_screen()

@reports_bp.route("/payments")
def payments(): return reports_service.get_reports_payments_screen()