from werkzeug.datastructures import MultiDict
from utils.safe_route import require_cr, check_connection
from utils.now import now
from flask import jsonify
from statistics import mean
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from utils.db import db
from manager.models.timezone import fuso
from sqlalchemy import func
from manager.models.sales import Sale
from manager.models.pos import Pos

class ReportsService:
    @check_connection
    @require_cr
    def get_reports_welcome_screen(self, bd:MultiDict, cr=None):
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
                    if sale.matricula == mat: real_func += sale.valor - sale.desconto # Vendas por funcionario
                    payments[sale.pagamento] += sale.valor - sale.desconto # Pega os metodos pagamentos

                # REFERENTE A MES PASSADO   
                if sale.data.month == mes_passado.month and sale.data.year == mes_passado.year: 
                    meta_dia[sale.data.day] += sale.valor - sale.desconto # Metas dos diaa

                # REFERENTE AO DIA DO MES ANTERIOR
                if sale.data.date() == mes_passado.date(): 
                    meta_clientes += 1 # Meta de atendimento de clientes

                # REFERENTE AO DIA ATUAL
                if sale.data.date() == data.date(): 
                    real_dia += sale.valor - sale.desconto # O real di dua
                    real_clientes += 1 # Real de Clientes
                
                # Todos os periodos
                cont_vendas += 1
                total_vendas += sale.valor - sale.desconto

            if meta_dia: media_meta_dia = mean(meta_dia.values())
            if meta_mes: media_meta_mes = mean(meta_mes.values())
            meta_ticket_medio = total_vendas / cont_vendas

            # =================== Seta na response as metricas
            return jsonify({
                "metas": {
                    "dia": media_meta_dia if meta_dia else 0,
                    "mes": media_meta_mes if meta_mes else 0,
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

    # @check_connection
    @require_cr
    def get_reports_payments_screen(self, bd:MultiDict, cr=None):
        filter = bd.get("filter") # Pega o filtro de resposta
        date = now(fuso(cr)) # Data atual de acordp com o timezone da loja
        res = defaultdict(int) # Reponse esperada
        res["payments"] = defaultdict(int)
        if filter:
            # ============== DATA
            match filter:
                case "day":
                    init_date = date.replace(hour=0, minute=0, second=0) # Define a hora de inicio
                    end_date = date.replace(hour=23, minute=59, second=59) # Define a hora final do filtro
                case "week":
                    init_date = date.replace(day=date.day - 7 ,hour=0, minute=0, second=0) # Define a hora de inicio
                    end_date = date.replace(hour=23, minute=59, second=59) # Defina a hora final do filtro
                case "month":
                    init_date = date.replace(day=1, hour=0, minute=0, second=0) # Define a hora de inicio
                    end_date = date.replace(hour=23, minute=59, second=59) # Defina a hora final do filtro
                    
            # ============== CONSULTA
            payments = db.session.query( Sale.pagamento, Sale.tipo, func.sum(Sale.valor - Sale.desconto).label("soma"), func.count(Sale.id).label("total") # SELECT
            ).filter( Sale.cr == cr, Sale.data >= init_date, Sale.data < end_date, # WHERE
            ).group_by( Sale.pagamento, Sale.tipo # GROUP BY
            ).all() # Obtem todos os registros de acordo com a consultaa
            pos = Pos.query.filter_by(cr=cr).first()
            for payment in payments: # Itera sobre a response
                res["orders"] += payment.soma if payment.tipo == "OS" else 0 # Total do valor de ORDENS DE SERVIÇO
                res["orders_count"] += payment.total if payment.tipo == "OS" else 0 # Total de contagem de OS
                res["products"] += payment.soma if payment.tipo == "PRODUTOS" else 0 # Total do valor de PRODUTOS
                res["product_count"] += payment.total if payment.tipo == "PRODUTOS" else 0 # Total de contagem
                res["payments"][payment.pagamento.lower()] += payment.soma # Adiciona o total por tipo
                res["total"] += payment.soma # Adiciona o total dos metodos de pagamento
                res["total_count"] += payment.total # Total de vendas em contagem
                res["opening"] = pos.abertura if pos else "Fechado"
            return jsonify(res), 200 # Retorna Sucesso 200
        return jsonify("Filtro obrigatorio"), 400 # Retorna BAD REQUEST - 400