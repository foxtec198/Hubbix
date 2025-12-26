from flask import Blueprint, request as rq, jsonify
from manager.services.pos_service import PosService

pos_bp = Blueprint("Caixa", __name__)
pos_service = PosService()

@pos_bp.route("", methods=['GET', 'POST', 'PATCH', 'DELETE'])
@pos_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return pos_service.status(rq.args) # Obtem o status do caixa
        case "POST": return pos_service.open(rq.get_json()) # Abre o dia do caixa
        case "PATCH": return pos_service.append(rq.get_json(), rq.headers) # Atualiza o valor do Caixa (Somatório)
        case "DELETE": return pos_service.close(rq.args, rq.headers) # Fecha o caixa do dia

@pos_bp.route("/last_closed")
def check(): return pos_service.last_close()

@pos_bp.route("/mode", methods=["GET", "POST", "DELETE"])
def mode():
    match rq.method:
        case "GET": return pos_service.get_products() # Obtem os produtos do Modo Caixa
        case "POST": return pos_service.set_products(rq.args.get("ean")) # Seta um produto, ou caso ja exista aumenta a quantidade em +1
        case "DELETE": return pos_service.clean_pos() # Limpa os prods por CR