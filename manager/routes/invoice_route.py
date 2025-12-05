from flask import Blueprint, request as rq, jsonify
from manager.services.invoice_service import InvoiceService

invoice_bp = Blueprint("NNF", __name__)
invoice_service = InvoiceService()

@invoice_bp.route("/", methods=["POST"])
def main():
    return invoice_service.create(rq.get_json(), rq.headers)