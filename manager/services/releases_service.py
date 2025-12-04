from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.safe_route import check_connection, require_cr
from utils.now import now
from manager.models.releases import Release
from manager.models.timezone import fuso

class ReleaseService:
    @check_connection
    @require_cr
    def get_releases(self, bd: MultiDict, hd: Headers, cr=None): # Logica para obter as saidas
        # Retorna uma lista de saidas ou uma saida especifica se o id for declarado
        id = bd.get("id")
        if id: return Release.query.filter_by(id=id, cr=cr).one().to_dict()
        else: return [release.to_dict() for release in Release.query.filter_by(cr=cr).all()]

    @check_connection
    @require_cr
    def create_release(self, bd: MultiDict, hd: Headers, cr=None): # Logica para criar um saida
        ...


    @check_connection
    @require_cr
    def update_release(self, bd: MultiDict, hd: Headers, cr=None): # Logica para atualizar uma saida
        ...

    @check_connection
    @require_cr
    def delete_release(self, bd: MultiDict, hd: Headers, cr=None): # Logica para excluir uma saida
        ...