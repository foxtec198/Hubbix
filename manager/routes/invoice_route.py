from flask import Blueprint, request as rq, jsonify
from manager.services.invoice_service import InvoiceService

invoice_bp = Blueprint("NNF", __name__)
invoice_service = InvoiceService()

@invoice_bp.route("", methods=["GET", "POST"])
def main(): 
    match rq.method:
        case "GET": return invoice_service.create_example() # Cria um exemplo de nota
        case "POST": return invoice_service.create_invoice() # Cria a nota não fiscal (NnF)
