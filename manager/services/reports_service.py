from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import require_cr, check_connection
from utils.db import cons
from utils.now import now, timedelta
from flask import jsonify
from statistics import mean
from manager.models.sales import Sale
from collections import defaultdict
from dateutil.relativedelta import relativedelta

@check_connection
class ReportsService:
    @require_cr
    def get_reports_welcome_screen(self, bd:MultiDict, hd:Headers, cr=None):
        mat = int(bd.get("mat")) # Matricula
        if mat:
            # =================== Vars
            data = now() # Data atual
            mes_passado = data - relativedelta(months=1) # Data do mes anterior
            meta_dia = defaultdict(int) # Metas dos dias
            meta_mes = defaultdict(int) # Metas dos meses
            payments = defaultdict(int) # Metodos de pagamentos
            real_mes = 0 
            real_dia = 0
            cont_vendas = 0
            total_vendas = 0
            meta_clientes = 0
            real_clientes = 0
            real_func = 0
            sales = Sale.query.filter_by(cr=cr).all()

            # =================== Logica
            for sale in sales:
                # REFERENTE AO ANO
                if sale.data.year == data.year: 
                    meta_mes[sale.data.month] += sale.valor - sale.desconto # Metas dos meses

                # REFERENTE AO MES ATUAL
                if sale.data.month == data.month and sale.data.year == data.year: 
                    real_mes += sale.valor - sale.desconto # Real no Mes
                    real_clientes += 1 # Real de Clientes
                    if sale.matricula == mat: real_func += sale.valor - sale.desconto # Vendas por funcionario
                    payments[sale.pagamento] += sale.valor - sale.desconto # Pega os metodos pagamentos

                # REFERENTE A MES PASSADO   
                if sale.data.month == mes_passado.month and sale.data.year == mes_passado.year: 
                    meta_dia[sale.data.day] += sale.valor - sale.desconto # Metas dos diaa
                    meta_clientes += 1 # Meta de atendimento de clientes

                # REFERENTE AO DIA ATUAL
                if sale.data.date() == data.date(): 
                    real_dia += sale.valor - sale.desconto # O real di dua
                
                # Todos os periodos
                cont_vendas += 1
                total_vendas += sale.valor - sale.desconto
            media_meta_dia = mean(meta_dia.values())
            media_meta_mes = mean(meta_mes.values())
            meta_ticket_medio = total_vendas / cont_vendas

            # =================== Seta na response as metricas
            return jsonify({
                "metas": {
                    "dia": media_meta_dia,
                    "mes": media_meta_mes,
                    "clientes": meta_clientes,
                    "ticket": meta_ticket_medio
                },
                "real": {
                    "dia": real_dia,
                    "mes": real_mes,
                    "clientes": real_clientes,
                    "func": real_func,
                    "pagamentos": payments
                }
            }), 200
        return jsonify("Matricula Obrigatória"), 400


