from flask import jsonify, Blueprint, request as rq, send_from_directory
from os import path, getcwd

files_bp = Blueprint("Arquivos", __name__)

@files_bp.route("/img/<sistema>/<filename>") # Rota geral para imagens (manager/gourmet)
def get_img(sistema, filename):
    try: return send_from_directory(path.join(getcwd(), sistema, "assets", "img"), filename)
    except Exception as err: return jsonify(err), 500

@files_bp.route("/videos/<sistema>/<filename>") # Rota geral para videos (manager/gourmet)
def get_videos(sistema, filename):
    try: return send_from_directory(path.join(getcwd(), sistema, "assets", "videos"), filename)
    except Exception as err: return jsonify(err), 500

@files_bp.route("/assets/<sistema>/<path>/<filename>") # Rota geral para SRCs (manager/gourmet)
def get_src(sistema, paths, filename):
    try: return send_from_directory(path.join(getcwd(), sistema, "assets", paths), filename)
    except Exception as err: return jsonify(err), 500

@files_bp.route("/qrpix/<sistema>/<filename>") # Rota geral para QRs de PIX (manager/gourmet)
def get_qr(sistema, filename):
    try: return send_from_directory(path.join(getcwd(), sistema, "assets", "qrpix"), filename)
    except Exception as err: return jsonify(err), 500

@files_bp.route("/nnf/<filename>") # Rota geral para Notas não Fiscais (manager)
def get_nnf(filename):
    try: return send_from_directory(path.join(getcwd(), "manager", "assets", "nnfs"), filename)
    except Exception as err: return jsonify(err), 500

