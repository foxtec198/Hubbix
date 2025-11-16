from manager.models.config import Config
from flask import Blueprint, jsonify, request as rq

product_bp = Blueprint("Produtos", __name__)

@product_bp.route("/")
def main():
    return jsonify("Sucesso")
