from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import require_cr, check_connection
from utils.db import cons
from utils.now import now, timedelta
from flask import jsonify

@check_connection
class ReportsService:
    @require_cr
    def get_reports_welcome_screen(self, bd:MultiDict, hd:Headers, cr=None):
        # =================== Vars
        response = {}
        data = now()
        mes_atual = f"{data.month}-{data.year}"
        mes_meta = f"{data.month - 1}-{data.year}"
        dia_atual = f"{data.day}-{data.month}-{data.year}"
        dia_meta = f"{data.day-1}-{data.month - 1}-{data.year}"
        mat = bd.get("mat")

        # =================== Consultas
        # Obtem a meta referente ao mes passado
        meta_mes = cons("select sum(valor - desconto) from vendas where to_char(data, 'MM-YYYY') = '%s' and cr = '%s'", (mes_meta, cr), all=False)[0]
        # Obtem o valor de venda atual
        total_mes = cons("select sum(valor - desconto) from vendas where to_char(data, 'MM-YYYY') = '%s' and cr = '%s'", (mes_atual, cr), all=False)[0]

        # Seta na response os valores
        response["meta_mes"] = meta_mes if meta_mes else 0
        response["total_mes"] = total_mes if total_mes else 0

        # Obtem a meta do dia e o ticket medio com base no mes passado
        meta_dia = cons("select sum(valor - desconto) from vendas where to_char(data, 'DD-MM-YYYY') = '%s' and cr = '%s'", (dia_meta, cr), all=False)[0]
        contagem_vendas = cons("select distinct count(id) from vendas where to_char(data, 'DD-MM-YYYY') = '%s' and cr = '%s'", (dia_meta, cr), all=False)[0]
        # Obtem o total de vendas no dia atual
        total_dia = cons("select sum(valor - desconto) from vendas where to_char(data, 'DD-MM-YYYY') = '%s' and cr = '%s'", (dia_atual, cr), all=False)[0]

        # Seta na response os valores
        response["meta_dia"] = meta_dia if meta_dia else 0
        response["total_dia"] = total_dia if total_dia else 0
        response["meta_ticket"] = meta_dia / contagem_vendas

        # Obtem o total de vendas por funcionario no mes
        employee_sales = cons("select sum(valor - desconto) from vendas where cr = '%s' and matricula = %s and tp_char(data, 'MM-YYYY') = '%s'", (cr, mat, mes_atual))

        # Repassa o valor pra response
        response["func_vendas"] = employee_sales

        # =================== Retorno
        return jsonify(response)


