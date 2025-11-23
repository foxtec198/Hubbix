# Utils
from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from utils.now import now, timedelta
from utils.check_cr import check_cr
from utils.check_field import check_field
from utils.db import cons, db
from flask import jsonify
from os import path, getcwd, remove
from PIL import Image, ImageDraw, ImageFont

# Models
from manager.models.service_order import ServiceOrder # A propira OS
from manager.models.cash_register import CashRegister # Caixa
from manager.models.employess import Employee # Funcionarios
from manager.models.config import Config # Configurações
from manager.models.clients import Client # Clientes
from manager.models.view_service_order import vwOS # View
from models.store_model import Store # Lojas

class ServiceOrderServices:
    def get(self, bd:MultiDict, hd:Headers): # Pega as OS fultrando por status e CR
        cr = hd.get('cr', False)
        status = bd.get('status', False)
        id = bd.get("id", False)
        if check_cr(cr):
            if id: return jsonify([o.to_dict() for o in vwOS.query.filter_by(id=id).all()])
            if not status: return jsonify(vwOS.search_by_cr(cr))
            if status == 'EXPIRADA': return jsonify(vwOS.get_expireds(cr, (now() - timedelta(90)).strftime("%m-%Y")))
            elif status: return jsonify(vwOS.search_by_status(status, cr))
        return jsonify('Loja inexistente!'), 401

    def create(self, bd:MultiDict, hd:Headers): # Cria um ordem de serviço
        cr = hd.get("cr", False)
        gc = hd.get('gc')
        if check_cr(cr):
            # Dados do Aparelho
            modelo = bd.get('modelo')
            cor = bd.get('cor', "")
            marca = bd.get('marca', "")

            # Sobre o serviço com o aparelho
            status = bd.get('status', "")
            relato = bd.get('relato', "").upper()
            tipo = bd.get('tipo', "").upper()
            obs = bd.get('obs', "").upper()

            # Dados da OS
            id_client = bd.get('cliente_id')
            retirada = bd.get('retirada', "0000/00/00")
            ligar = bd.get('ligar', True)
            st_os = bd.get('st_os', "ABERTA")
            valor = bd.get('valor')
            matricula = bd.get('matricula')

            # Dados que serão obrigatórios! 
            ok, error = check_field(
                modelo = modelo,
                cor = cor,
                marca = marca,
                retirada = retirada,
                valor = valor,
                matricula = matricula
            )
            
            if ok: # Confirma os dados obrigatorios passados acima
                if CashRegister.check(cr): # Confirma se o caixa esta aberto
                    atendente = Employee.query.filter_by(matricula=matricula, cr=cr).one() # Pega o nome do atendente pela matricula
                    # Cria o Modelo da Ordem
                    os = ServiceOrder()
                    os.id_cliente = id_client
                    os.modelo = modelo 
                    os.cor = cor.upper()
                    os.marca = marca.upper()
                    os.status = status.upper()
                    os.tipo = tipo 
                    os.obs = obs, 
                    os.relato = relato 
                    os.entrega = f"{retirada.replace('/','-')} 00:00:00",
                    os.abertura = now(), 
                    os.ligar = ligar
                    os.situacao = st_os.upper(),
                    os.valor = valor
                    os.atendente = atendente.nome.upper()
                    os.grupodecliente = gc 
                    os.cr = cr

                    # Faz a adic~çao ao bd
                    db.session.add(os)
                    db.session.commit()
                    self.make_so(os.id, cr)
                    return jsonify({
                        'msg':"Ordem aberta com sucesso!",
                        'os': os.id
                    }), 200
                return jsonify("Caixa fechado!"), 401
            return jsonify(error), 400
        return jsonify("Loja Inexistente"), 401
    
    def update(self, bd:MultiDict, hd:Headers): # Atualiza os dados das Ordens
        # Cred
        cr = hd.get('cr', False)

        # Dados
        id = bd.get('id', False)
        status_os = bd.get('status_os', "ABERTA")
        modelo = bd.get('modelo')
        cor = bd.get('cor')
        marca = bd.get('marca')
        valor = bd.get('valor')
        cpf = bd.get('cpf')
        servico = bd.get('servico')
        imei = bd.get('imei')

        if check_cr(cr): # Confere se a loja esta ok
            if CashRegister.check(cr): # Retorna se o caixa está aberto
                if id:
                    os = ServiceOrder.query.filter_by(id = id).one() # Pega os dados da OS - Se existente
                    vos = vwOS.query.filter_by(id = id).one()
                    
                    if os: # Confere se a OS existe antes de dar continuidade
                        client = Client.query.filter_by(cpf=vos.cpf, cr=cr).one() # Pega os dados do cliente

                        #  Atualiza os Dados da Ordem
                        if status_os: os.status = status_os
                        if modelo: os.modelo = modelo.upper()
                        if cor: os.cor = cor.upper()
                        if marca: os.marca = marca.upper()
                        if valor: os.valor = valor
                        if servico: os.servico = servico
                        if imei: os.imei = imei
                        
                        # Atualiza os dados do CLiente
                        if modelo: client.modelo = modelo.upper()
                        if cor: client.cor = cor.upper()
                        if marca: client.marca = marca.upper()
                        if imei: client.imei = imei
                        
                        try: remove(f'manager/assets/os/os_{id}.pdf')
                        except: ...
                        
                        self.make_so(id, cr)
                        db.session.commit()
                        
                        return jsonify("OS:%s editada com sucesso!"%id), 200
                    return jsonify("ID Obrigatório!"), 400
                return jsonify("Ordem não localizada, favor verificar o numeor de ordem"), 401
            return jsonify("Primeiro abra o caixa!"), 401
        return jsonify("Loja inexistente!"), 401
    
    def delete(self, bd:MultiDict,hd:Headers): # Ao inves de Deletar seta como Cancelado
        id = bd.get("id", False)
        cr = hd.get("cr", False)
        if check_cr(cr): # Confere se a loja esta OK
            if id: # Confere o ID da OS
                os = ServiceOrder.query.filter_by(id=id).one()
                os.status = "CANCELADA"
                db.session.commit()
                return jsonify("Ordem Cancelada com sucesso!")
            return jsonify("ID Obrigatorio"), 400
        return jsonify("Loja inexistente"), 401
    
    def resize(self, img, scale): # faz o resize da logo pra utilizar na OS
        x = int(img.size[0]) / int(scale)
        y = int(img.size[1]) / int(scale)
        newImg = img.resize((int(x), int(y)))
        return newImg
    
    def make_so(self, id, cr): # Cria o arquivo da Ordem de Serviço
        res = cons("""SELECT
            C.Nome, C.CPF, C.Endereco, C.Telefone,
            OS.Modelo, OS.Cor, OS.Marca, OS.IMEI, OS.Atendente, to_char(OS.Abertura, 'DD/MM/YYYY HH24:MI'),
            OS.status, OS.tipo, OS.obs, OS.relato, OS.ligar, OS.entrega, OS.valor, OS.Situacao
            FROM os OS
            INNER JOIN clientes C
                ON C.id = OS.id_cliente
            WHERE OS.id = %s
            AND OS.cr = '%s'""", (id, cr), all=False)
        if res:
            nome, cpf, end, telefone, modeloC, cor, marca, imei, func, dataA, stA, tipoS, obsOs, relatoOs, ligar, dataE, valor, situacao = res
            numOs = id
            store = Store.query.filter_by(cr=cr).one()
            nome_loja = store.nome_loja
            telefone_loja = store.telefone
            endereco_loja = Store.get_endereco(cr)
            config = Config.query.filter_by(cr=cr).one()
            logo = config.logo
            escala = config.escala

            status = stA.split(',')
            tipo = tipoS.replace(',', ' ')
            
            if len(str(cpf)) > 11: cpf = ''
            modelo = Image.open(path.join(getcwd(), 'manager', 'assets', 'img', 'modeloOS.png'))
            draw = ImageDraw.Draw(modelo)
            ft = ImageFont.truetype('manager/assets/fonts/Roboto-Bold.ttf', 22)
            ftTiny = ImageFont.truetype('manager/assets/fonts/Roboto-Bold.ttf', 22)
            ft2 = ImageFont.truetype('manager/assets/fonts/Roboto-Bold.ttf', 25)
            ftOS = ImageFont.truetype('manager/assets/fonts/coolvetica rg.otf', 45)
            fg = 'black'

            # APLICAR LOGO
            logo = Image.open(path.join(getcwd(), 'manager', 'assets', 'img', logo))
            logo = self.resize(logo, escala)
            try: modelo.paste(logo, (40,40), logo)
            except: modelo.paste(logo, (40,40))

            # APLICAR NOME LOJA
            loja = f'{nome_loja} - {endereco_loja} - Telefone: {telefone_loja}'
            draw.text((120, 242), loja, fill=fg, font=ft)

            # Numero da OS
            draw.text((765, 50), f'N°: {numOs}', fill='#e63946', font=ftOS)

            # Dados Pessoais
            draw.text((150, 290), str(nome), fill=fg, font=ft)
            draw.text((870, 290), str(cpf), fill=fg, font=ft)
            draw.text((180, 340), str(end), fill=fg, font=ft)
            draw.text((170, 398), str(telefone), fill=fg, font=ft)
            draw.text((565, 398), str(modeloC), fill=fg, font=ft)
            draw.text((855, 398), str(cor), fill=fg, font=ft)
            draw.text((1160, 398), str(marca), fill=fg, font=ft)
            draw.text((120, 453), str(imei), fill=fg, font=ft)
            draw.text((1020, 453), str(dataA), fill=fg, font=ft)
            draw.text((660, 453), str(situacao), fill=fg, font=ft)

            draw.text((190, 505), str(func.upper()), fill=fg, font=ft)
            if(ligar): draw.text((665, 505), 'Sim', fill=fg, font=ft )
            else: draw.text((665, 505), 'Não', fill=fg, font=ft )
            draw.text((1030, 505), dataE.strftime('%d/%m/%Y'), fill=fg, font=ft )
            draw.text((800, 555), f'Valor da Ordem de Serviço: R$ {self.formatNumber(valor)}', fill=fg, font=ft2 )

            # Status
            x = 40
            cont = 0
            y = 600
            for i in status:
                if(len(i) > 35): draw.text((x, y), f'- {i.capitalize()[:35]}...', fill=fg, font=ftTiny )
                else: draw.text((x, y), f'- {i.capitalize()}', fill=fg, font=ftTiny )
                y += 30
                cont += 1
                if cont == 7: 
                    x += 420
                    y = 600
                if cont == 14: 
                    x += 450
                    y = 600
            
            tt1 = 40
            tt2 = 40
            relatoOs = relatoOs.capitalize()
            if len(relatoOs) >= tt1:
                draw.text((tt2, 850), f'- {relatoOs[:tt1]}', fill=fg, font=ftTiny)
                draw.text((tt2, 870), f'{relatoOs[tt1:tt1*2]}', fill=fg, font=ftTiny)
                draw.text((tt2, 890), f'{relatoOs[tt1*2:tt1*3]}', fill=fg, font=ftTiny)
                draw.text((tt2, 910), f'{relatoOs[tt1*3:tt1*4]}', fill=fg, font=ftTiny)
                draw.text((tt2, 930), f'{relatoOs[tt1*4:tt1*5]}', fill=fg, font=ftTiny)
                draw.text((tt2, 950), f'{relatoOs[tt1*5:tt1*6]}', fill=fg, font=ftTiny)
            else: draw.text((tt2, 850), f'- {relatoOs}', fill=fg, font=ftTiny )

            tt1 = 40
            tt2 = 465
            obsOs = obsOs.capitalize()
            if len(obsOs) >= tt1:
                draw.text((tt2, 850), f'- {obsOs[:tt1]}', fill=fg, font=ftTiny)
                draw.text((tt2, 870), f'{obsOs[tt1:tt1*2]}', fill=fg, font=ftTiny)
                draw.text((tt2, 890), f'{obsOs[tt1*2:tt1*3]}', fill=fg, font=ftTiny)
                draw.text((tt2, 910), f'{obsOs[tt1*3:tt1*4]}', fill=fg, font=ftTiny)
                draw.text((tt2, 930), f'{obsOs[tt1*4:tt1*5]}', fill=fg, font=ftTiny)
                draw.text((tt2, 950), f'{obsOs[tt1*5:tt1*6]}', fill=fg, font=ftTiny)
            else: draw.text((tt2, 850), f'- {obsOs}', fill=fg, font=ftTiny)
            

            tt1 = 45
            tt2 = 910
            tipo = tipo.capitalize().replace(' \n', ', ')
            tipo = tipo.replace('\n', ', ')

            if len(tipo) >= tt1:
                draw.text((tt2, 850), f'- {tipo[:tt1]}', fill=fg, font=ftTiny)
                draw.text((tt2, 870), f'{tipo[tt1:tt1*2]}', fill=fg, font=ftTiny)
                draw.text((tt2, 890), f'{tipo[tt1*2:tt1*3]}', fill=fg, font=ftTiny)
                draw.text((tt2, 910), f'{tipo[tt1*3:tt1*4]}', fill=fg, font=ftTiny)
                draw.text((tt2, 930), f'{tipo[tt1*4:tt1*5]}', fill=fg, font=ftTiny)
                draw.text((tt2, 950), f'{tipo[tt1*5:tt1*6]}', fill=fg, font=ftTiny)
            else: draw.text((tt2, 850), f'- {tipo}', fill=fg, font=ftTiny)

            # SALVAR OS
            arquivo = f'manager/assets/os/os_{numOs}.pdf'
            modelo.save(arquivo)
            return arquivo
        return 'Nao encontramos esta Ordem em nosso banco de dados!'

    def formatNumber(self, number:float = 0): # Função criada para usar o K, M, B ao inves de manter o numero inteiro!
        if number > 0 and number < 1000: return round(number, 2)

        # Unidade de Milhar
        elif number >= 1000 and number < 10000: return f'{str(number)[0]}.{str(number)[1]}K'
        elif number >= 10000 and number < 100000: return f'{str(number)[:2]}.{str(number)[2]}K'
        elif number >= 100000 and number < 1000000: return f'{str(number)[:3]}.{str(number)[3]}K'

        # Unidade de milhão
        elif number >= 1000000 and number < 10000000: return f'{str(number)[0]}.{str(number)[1]}M'
        elif number >= 10000000 and number < 100000000: return f'{str(number)[:2]}.{str(number)[2]}M'
        elif number >= 100000000 and number < 1000000000: return f'{str(number)[:3]}.{str(number)[3]}M'

        # Unidade de Bilhão
        elif number >= 1000000000 and number < 10000000000: return f'{str(number)[0]}.{str(number)[1]}B'
        elif number >= 10000000000 and number < 100000000000: return f'{str(number)[:2]}.{str(number)[2]}B'
        elif number >= 100000000000 and number < 1000000000000: return f'{str(number)[:3]}.{str(number)[3]}B'
        else: return round(number, 2)
