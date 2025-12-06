from werkzeug.datastructures import MultiDict, Headers
from analytics.models.views import View
from utils.db import db, cons
from collections import defaultdict
from flask import jsonify, request as rq
from utils.now import now

class AnalyticService:
    def get(self, bd:MultiDict, hd:Headers): # Retorna as informações para Dashboard e detalhamento de Views
        # Variaveis
        unit_id = hd.get("unit_id") # Id da Unidade
        client_id = bd.get("client_id") # Cliente
        views = [] # Cria um lista vazia
        days = set() # Cria um set de Dias 
        info_days_dashboard = defaultdict(lambda: {'click':0, 'form':0, 'view':0}) # Faz cm que o set se torne um dicionario com os tipos

        if unit_id:
            # Confere se tem o client ID, caso contrario retorna sem filtro
            if client_id: 
                views_response = cons("""
                    select v.type, c.name, u.name, v.date, v.ip
                    from views v 
                    inner join clients c 
                        on v.client_id = c.id
                    inner join units u
                        on v.unit_id = u.id
                    where u.id = %s
                    and c.id = %s
                    order by v.date desc
                    """, (unit_id, client_id), all=True, db="analytics"
                )
            else:
                views_response = cons("""
                    select v.type, c.name, u.name, v.date, v.ip
                    from views v 
                    inner join clients c 
                        on v.client_id = c.id
                    inner join units u
                        on v.unit_id = u.id
                    where u.id = %s
                    order by v.date desc
                    """, (unit_id), all=True, db="analytics"
                )
            for type, name, unit, date, ip in views_response:
                views.append({
                    'type': type,
                    'name': name,
                    'unidade': unit,
                    'data': date,
                    'ip': ip
                })

            # Consulta dados para o dashborad
            infos_dashboard = cons("select DISTINCT to_char(date, 'DD') as dataa, count(type) as total, type from views where unit_id = %s group by dataa, type order by dataa asc", unit_id, all=True)

            # Trata os dados da Consulta do Dashboard
            for day, quant, type in infos_dashboard:
                days.add(day) # Adiciona os dias do BD a variavel "days"
                info_days_dashboard[day][type.lower()] = quant
            days = sorted(days) # Faz com que os dias fiquem em ordem crescente

            # Separa os dias por tipos
            clicks = [info_days_dashboard[day]['click'] for day in days]
            forms  = [info_days_dashboard[day]['form'] for day in days]
            view  = [info_days_dashboard[day]['view'] for day in days]

            views.append({
                'dash':{
                    'dias': days,
                    'clicks': clicks,
                    'forms': forms,
                    'views': view
                }
            })

            return jsonify(views), 200
        return jsonify("Unit_id obrigatorio"), 400

    def set(self, bd:MultiDict, hd:Headers): # Seta uma View, Form ou Click
        view = View()
        type = bd.get("type")
        client_id = bd.get("client_id")
        unit_id = hd.get("unit_id")
        ip = rq.headers.get('X-Forwarded-For').split(',')[0]
        data = now()

    