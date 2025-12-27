from manager.models.categories import Categorie, db
from utils.safe_route import require_cr, check_connection
from werkzeug.datastructures import MultiDict
from flask import jsonify, Response

@check_connection
class CategoriesService:
    @require_cr
    def get(self, bd:MultiDict, cr="Não declarar ao chamar a função") -> tuple:
        """
        Docstring for get
        
        :param self: Description
        :param bd: Description
        :type bd: MultiDict
        :param cr: Parametro obrigatório non header (Não declarar ao chamar a função!!!!!!!!!)
        :return: Retorna a categoria e o codigo (MSG, CODE)
        :rtype: tuple[Response, Literal[200, 404]]
        """
        id = bd.get("id") # Obtem o id passado no args (Não origatório)
        if id: # Se o id foi passado faz o teste
            categorie = Categorie._search_by_id(id, cr) # Ontem a categoria por id
            return jsonify(categorie), 200 if categorie else jsonify("Categoria não encontrada"), 404 # Confirma se encontrou a categoria no banco se nao retorna 404 - NOT FOUND
        else: return jsonify(Categorie._search_by_cr(cr)), 200 # Retornas as categorias por CR (loja)
