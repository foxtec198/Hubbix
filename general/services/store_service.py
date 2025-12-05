from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import check_connection, require_cr
from general.models.store import Store
from flask import jsonify

class StoreService:
    @check_connection
    @require_cr
    def get_store_data(self, cr=None): # Retorna os dados da Loja
        store = Store.query.filter_by(cr=cr).first()
        if store: return jsonify(store.to_dict())
        return jsonify("Loja nao encontrada"), 404

    @check_connection
    @require_cr
    def create_store(self, bd:MultiDict, hd:Headers, cr=None):
        ...

    @check_connection
    @require_cr
    def update_store(self, bd:MultiDict, hd:Headers, cr=None):
        ...

    @check_connection
    @require_cr
    def delete_store(self, bd:MultiDict, hd:Headers, cr=None):
        ...
