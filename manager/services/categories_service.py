from manager.models.categories import Categorie
from utils.safe_route import safe_route
from flask import jsonify, request as rq

class CategoriesService:
    @safe_route
    def get(self, token_data) -> tuple:
        """
        Docstring for get
        
        :param self: Description
        :param bd: Description
        :type bd: MultiDict
        :param cr: Parametro obrigatório non header (Não declarar ao chamar a função!!!!!!!!!)
        :return: Retorna a categoria e o codigo (MSG, CODE)
        :rtype: tuple[Response, Literal[200, 404]]
        """
        cr = token_data.get("cr")
        id = rq.args.get("id") # Obtem o id passado no args (Não origatório)
        if id: # Se o id foi passado faz o teste
            categorie = Categorie._search_by_id(id, cr) # Ontem a categoria por id
            return jsonify(categorie), 200 if categorie else jsonify("Categoria não encontrada"), 404 # Confirma se encontrou a categoria no banco se nao retorna 404 - NOT FOUND
        else: return jsonify(Categorie._search_by_cr(cr)), 200 # Retornas as categorias por CR (loja)
