from flask import Blueprint, request as rq, jsonify

brand_bp = Blueprint("Marcas", __name__)

@brand_bp.route("/")
def main():
    return jsonify("")
    