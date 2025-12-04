from requests import get, post, put, patch
from json import dumps
from utils.now import now
from qrcode import make
from os import environ
from dotenv import load_dotenv
from flask import jsonify

url = "https://api.mercadopago.com/"
load_dotenv()

class MP():
    # Pega o ID de desenvolvedor
    def __init__(self): self.user_id = self.get_id()

    # Get Access token
    def get_access_token(self):
        body = {
            "client_secret": environ['client_secret'],
            "client_id": environ['client_id'],
            "grant_type": "client_credentials",
        }

        response = post(url + 'oauth/token', data=dumps(body))
        return response.json()['access_token']
    
    # Orders
    def create_order(self, valor, cr):
        valor = float(valor)
        external_pos_id = cr.replace("-", "").replace(" ", "")

        key = external_pos_id + 'KEY' + now().strftime('%Y%m%d%H%M%S')
        body = {
            "type": "qr",
            "total_amount": f"{valor:.2f}",
            "description": "Point New Land",
            "external_reference": key,
            "expiration_time": "PT16M",
            "config": {
                "qr": {
                    "external_pos_id": external_pos_id,
                    "mode": "static"
                }
            },
            "transactions": {
                "payments": [
                    {
                        "amount": f"{valor:.2f}"
                    }
                ]
            },
        }

        headers = {
            "Authorization":f"Bearer {self.get_access_token()}",
            "X-Idempotency-Key": key
        }

        try:
            res = post(url + '/v1/orders', headers=headers, data=dumps(body))
            id = res.json()['id']
            dd = {'id': id, 'key': key}
            return dd
        
        except Exception as e: return e

    def create_qr(self, key, valor, cr):
        if self.user_id:
            if cr:
                if key:
                    if valor:
                        valor = float(valor)
                        external_pos_id = cr.replace("-", "").replace(" ", "")

                        headers = {"Authorization": f"Bearer {self.get_access_token()}"}
                        body = {
                            "external_reference": key,
                            "title": "HBX QR",
                            "description": "Realize o pagamento em até 60seg.",
                            # "notification_url": f"https://api.hubbix.com.br/notifications",
                            "total_amount": valor,
                            'items': [
                                {
                                    "sku_number": "0",
                                    "category": "marketplace",
                                    "title": "Hubbix Service",
                                    "description": "Isto é um PIX do sistema da Hubbix",
                                    "unit_price": valor,
                                    "quantity": 1,
                                    "unit_measure": "unit",
                                    "total_amount": valor
                                }
                            ]
                        }

                        res = put(
                            url + f'instore/orders/qr/seller/collectors/{self.user_id}/pos/{external_pos_id}/qrs',
                            headers=headers, data=dumps(body)
                        )

                        try:
                            js = res.json()
                            img = make(js['qr_data'])
                            caminho = 'qrpix/' + external_pos_id + key + '.png'
                            img.save(caminho)
                            return jsonify(caminho), 200
                        except Exception as e: return jsonify(str(e)), 500
                    return jsonify("Valor obrigatorio"), 400
                return jsonify("Chave obrigatoria"), 400
            return jsonify("CR obrigatorio"), 400
        return jsonify("Identificação de Usuario obrigatorio"), 401
    
    def get_order(self, id):
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-type": "application/json"
        }

        res = get(url + f'v1/orders/{id}', headers=headers)
        return res.json()
    
    def get_merchant_order(self, key):
        res = get(
            f'https://api.mercadopago.com/merchant_orders/search?external_reference={key}',
            headers={"Authorization": f"Bearer {self.get_access_token()}"}
        )
        return res.json()
    
    # POS
    def create_pos(self):
        idLoja = 67887103
        external_id = '1MSOFICINADOCELULAR'
        nomeloja = 'Oficina do cllr'
        body = {
            "name": f"Caixa - {nomeloja}",
            "fixed_amount": False,
            "store_id": idLoja,  # ID da loja já cadastrada
            "external_id": external_id  # Esse será o seu external_pos_id
        }

        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-type": "application/json"
        }

        res = post(url + 'pos', headers=headers, data=dumps(body))
        print(res.json())

    def get_pos(self):
        headers = {"Authorization": f"Bearer {self.get_access_token()}"}

        res = get(url + 'pos', headers=headers)
        return res.json()

    # Stores
    def create_store(self, bd, hd): # FUNÇÃO PRIMORDIAL
        cr = hd.get("cr")

        external_id = cr.replace("-","").replace(" ","")
        nome = bd.get("nome")
        numero = bd.get("numero")
        rua = bd.get("rua")
        cidade = bd.get("cidade")
        estado = bd.get("estado")
        latitude = bd.get("latitude")
        longitude = bd.get("longitude")

        headers = {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-type": "application/json"
        }
        body = {
            "name": nome,
            "external_id": external_id,
            "location":{
                "street_name": rua,
                "street_number": numero,
                "city_name": cidade,
                "state_name": estado,
                "latitude": latitude,
                "longitude": longitude,
                "reference": cr
            }
        }

        res = post(url + f'users/{self.user_id}/stores', data=dumps(body), headers=headers)
        return res.json()['id']

    def get_stores(self):
        headers={"Authorization": f"Bearer {self.get_access_token()}"}

        res = get(url + f"users/{self.user_id}/stores/search", headers=headers)
        return res.json()

    # Users
    def get_id(self):
        hd = {"Authorization": f"Bearer {self.get_access_token()}"}

        res = get(url + 'users/me', headers=hd)
        response = res.json()['id'] if res else False
        if res: return response, 200
        else: return res.json(), 400

    # Terminals - Maquininhas
    def list_terminals(self):
        hd = {"Authorization": f"Bearer {self.get_access_token()}",}

        # return get(url + 'terminals/v1/list', headers=hd).json()
        res = get(url + 'point/integration-api/devices', headers=hd)
        return res.json(), res.status_code

    def update_point_mode(self, id, mode:str ='PDV'):
        if id and mode:
            hd = {"Authorization": f"Bearer {self.get_access_token()}",}
            dd = {"operating_mode": mode}
            
            res = patch(url + f'point/integration-api/devices/{id}', headers=hd, data=dumps(dd))
            return res.json(), res.status_code
        return jsonify("Dados Obrigatorios"), 400