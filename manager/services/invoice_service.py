from utils.safe_route import check_connection, require_cr
from werkzeug.datastructures import Headers, MultiDict
from PIL import Image, ImageDraw, ImageFont
from general.models.store import Store
from manager.models.releases import Release
from manager.models.sales import Sale
from manager.models.clients import Client
from manager.models.employess import Employee
from utils.to_real import to_real
from os import getcwd, path
from utils.db import db
from sqlalchemy import func
from flask import jsonify
from utils.now import now
from manager.models.timezone import fuso

# ============== Fontes
coolvetica = path.join(getcwd(), "manager", "assets", "fonts", "coolvetica.otf")
bebas = path.join(getcwd(), "manager", "assets", "fonts", "BebasNeue-Regular.ttf")
Astonpoliz = path.join(getcwd(), "manager", "assets", "fonts", "Astonpoliz.otf")

class InvoiceService:
    def __init__(self): 
        # Define a altura e largura inicial
        self.font = ImageFont.truetype(Astonpoliz, 10)
        self.largura = 380
        self.altura = 380

    def get_x(self, texto:str): # Centraliza o texto
        """
        Docstring for Get_X

        :param texto: String que deverá ser retorna seu devido X centralizado
        :type texto: str

        :return: Ex: 2 | 0.05
        :rtype: INT | FLOAT
        """
        texto = str(texto) # Converte para string caso seja numero
        bbox = self.draw.textbbox((0, 0), texto, font= self.font) # Cria o BBOX usando Pillow

        # retorna a (LARGURA - (TEXTO_X - TEXTO_Y)) // 2
        return (self.largura - (bbox[2] - bbox[0])) // 2 

    def draw_text(self, x, y, texto:str, font=None): # Escreve o texto na img
        """
        Docstring for Draw Text - Facilitador de codigo para inserção de texto

        :param x: Numero onde será posicionado o texto (Eixo X)
        :type x: int | float
        :param y: Numero onde será posicionado o texto (Eixo Y)
        :type y: int | float
        :param text: Texto a ser posicionado
        :type text: str
        :param font: Fonte a ser utilizada
        :type font: path.join(localização da fonte) # Chamada de pasta segura
        """
        font = self.font if not font else font
        self.draw.text((x, y), str(texto), font=font, fill=(0, 0, 0))

    def separator_without_text(self, y, key='='): # Apenas separa com algum caractere
        # Caso precise alterar o modelo ou o tamanho, continua responsivo
        separador = key * self.largura # Separa de acordo com a largura da imagem
        self.draw_text(self.get_x(separador), y, separador) # Escreve o separador
    
    def separator_with_text(self, y, text:str): # Separa com texto no meio
        # Caso precise alterar o modelo ou o tamanho, continua responsivo
        txtl = len(text) # Obtem o tamanho do texto declarado
        total = self.largura + txtl # Obtem o total com a largura
        meio = (total - txtl ) // 2 # Pega exatamente o valor que deverá ser adionado aos lados do texto
        separador = '=' * meio + f" {text} " + '=' * meio  # Cria o texto com o spearador EX: ====== TEXTO =====
        self.draw_text(self.get_x(separador), y, separador) # Escreve o texto na imagem (Responsivo)
            
    def create_invoice_archive(self, store_name, cnpj, address, tel, employye, id_sale, date, client, cart, total, payment, cr, example:bool=False): # Cria o arquivo da nota
        # Dependendo do tamamho do carrinho modifica o tamnho do doc
        if cart: # Confima se tem um carrinho e itera sobre ele, aumentando o tamanho da altura conforme o necessário
            for i in range(1, len(cart) + 1): self.altura += 25 # 25 é um tamanho bom, da um espaçamento visualmente bonito
                    
        self.img = Image.new("RGB", (self.largura, self.altura), color=(255, 255, 255)) # Cria a imagem com as larguras e alturas e na cor branca
        self.draw = ImageDraw.Draw(self.img) # Utiliza da imagem criada acima para adicionar os elementos (Usando o DRAW do Pillow)

        # Carrega as fontes setadas no inicio do Documento
        fontTitulo = ImageFont.truetype(bebas, 18) # Bebas Nue
        fontSub = ImageFont.truetype(coolvetica, 11) # Coolvetica Sans Serif

        # ----------------------CABEÇALHO----------------------------
        self.draw_text(self.get_x(store_name), 15, store_name, fontTitulo) # Titulo - NOME DA LOJA
        self.draw_text(20, 40, f"CNPJ: {cnpj}") # CNPJ ou CPF
        self.draw_text(20, 60, f"Endereço: {address}") # Endereço
        self.draw_text(20, 80, f"Telefone: {tel}") # Telefone
        self.draw_text(20, 100, f"Atendente: {employye}") # Funcionario

        nSell = f"Venda N°{id_sale}" # Numero de Venda
        self.separator_without_text(120) # CRIA UM SEPARADOR SEM TEXTO
        self.draw_text(self.get_x(nSell), 130, nSell)
        self.separator_without_text(140) # CRIA UM SEPARADOR SEM TEXTO

        # ------------------------CORPO------------------------------
        self.draw_text(20, 160, f"Data e Hora: {date}") # Data da Compra
        self.draw_text(20, 180, f"Cliente: {client}") # Nome do Cliente
        self.separator_with_text(200, 'PRODUTOS') # Cria um titulo com separador

        # Header da Tabela de Produtos
        self.draw_text(20, 220, "Item") # Header Nome do Item/Produto
        self.draw_text(230, 220, "Qtd.") # Header de Quantidade
        self.draw_text(280, 220, "Vlr.") # Header Valor
        self.draw_text(330, 220, "Subtotal") # Header Subtotal
        self.separator_without_text(230, '-') # Cria um separador para o corpo da tabela usando ifen

        # Body da Taneça de Produtos
        y = 240 # Tamanho padrão para inicio, tamanho ideal para todas lojas
        for item in cart: # Para cada produto no carrinho itera os dados
            self.draw_text(20, y, item['nome']) # Nome do Produto
            self.draw_text(230, y, str(item['quant'])) # Quantidade do produto
            self.draw_text(280, y, to_real(item['valor']))  # Valor do Produto com R$
            self.draw_text(330, y, to_real(item['valor'] * item['quant'])) # Valor total R$
            y += 20 # Adiciona um espaçamento de mais 20 para que os prods nao fiquem "grudados"

        self.separator_with_text(y, "PAGAMENTO") # Separa para o campo de Pagamento

        ttll = "Total da Venda" # Titulo do Total
        self.draw_text(self.get_x(ttll), y + 20, ttll) # Escreve o texto centralizado usando a função get_x adicionando 20 no eixo y para o espaçamento de linha
        self.draw_text(330, y + 20, to_real(total)) # Total em REAL não centralizado e com 20 de adição ao eixo y para espaçamento de linha

        mtlbl = 'Metodo de Pagamento' # Titulo do Metodo de Pagamento
        self.draw_text(self.get_x(mtlbl), y + 40, mtlbl) # Seta o texto centralizado com +40 no eixo Y para espaçamento de linha
        self.draw_text(330, y + 40, payment) # Metodo de Pagamento

        self.separator_without_text(y + 50, "-") # Separador sem texto usando ifen

        # ------------------------FOOTER------------------------------
        aviso = "*** Esse ticket não é documento fiscal ***" # Aviso sobre a Invoice
        self.draw_text(self.get_x(aviso), y + 60, aviso) # Escreve o aviso centralizado com +60 no eixo Y para espaçamento de linha

        agradecimento = "OBRIGADO E VOLTE SEMPRE!" # Agradecimento ao consumidor
        self.draw_text(self.get_x(agradecimento), y + 80, agradecimento, fontSub) # Escreve o agradecimento centralizado com +80 no Y para espaçamento de linha e com a fonte de subtitulo

        self.separator_without_text(y + 100, "-") # Separador sem texto usando ifen

        devby = "Desenvolvido por ®Hubbix Sistemas - hubbix.com.br" # Creditos
        self.draw_text(20, y + 120, devby) # Escreve o texto não centralizado com +120 de espaçamento
        
        if example: nome_arquivo = f'{cr}_exemplo.pdf' # Define o nome do arquivo de Exemplo
        else: nome_arquivo = f'{cr}_{id_sale}.pdf' # Define o nome do arquivo que será salvo
        caminhoImg = path.join(getcwd(), "manager", "assets", "nnfs", nome_arquivo) # Define a pasta segura onde será salvo
        self.img.save(caminhoImg) # Salva a imagem como PDF 
        return nome_arquivo # Retorna o nome do arquivo
    
    @check_connection
    @require_cr
    def create_example(self, cr = None): # Gera um exemplo de nota não fiscal
        arquivo = self.create_invoice_archive(
            "NOME DA LOJA", "12345678910111", "Endereço de EXemplo", "(DDD)TELEFONE",
            "NOME DO FUNCIONARIO", "1584", now(fuso(cr)), "NOME DO CLIENTE", 
            {"nome": "PRODUTO TESTE", "quantidade": 2, "valor": 20}, 40, "PIX", cr, True
        )
        return jsonify(arquivo)
    
    @check_connection
    @require_cr
    def create_invoice(self, bd:MultiDict, cr = None): # Cria a nota pelo ROUTE
        """
        Docstring for Create Invoice

        :param bd: Body(JSON) deve ser passado o Id da Venda para fazer a criação da invoice
        :type bd: MultiDict
        :param cr: Credencial da Loja declarada no Header (Não declarar na função!)
        :type cr: String - str()
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200 | 400 | 404]] 
        """
        id_venda = bd.get('id_venda') # ID da venda
        if id_venda: # Confere se foi declarado
            store = Store._search_by_cr(cr) # Obtem a loja por CR
            if store: # Confere se encontrou a loja
                releases = db.session.query(
                    Release.nome, # Nome da SAIDA - Produto/OS
                    func.count(Release.id).label("quantidade"), # Contagem de produtos - Quantidade 
                    Release.valor.label("valor_produto"), # Valor do Produto
                    Sale.data, # Data da Venda
                    Sale.valor, # Valor da Venda
                    Sale.pagamento, # Pagamento
                    Employee.nome.label("atendente"), # Atendente da venda
                    Client.nome.label("cliente") # Nome do Cliente
                ).join(
                    Sale, Sale.id == Release.id_venda # Inner join por ID
                ).join(
                    Client, Client.id == Sale.id_cliente # Inner join por ID
                ).join(
                    Employee, Employee.matricula == Sale.matricula # Inner join por Matricula
                ).filter(
                    Sale.id == id_venda, # Filtra por id
                    Sale.cr == cr # Filtra por CR
                ).order_by(
                    Sale.data.desc() # Ordena pela data decrescente
                ).group_by( # Agrupa os items da forma correta
                    Release.nome, Release.valor, Sale.data, 
                    Sale.valor, Sale.pagamento, Employee.nome,
                    Client.nome
                ).all() # Pega todos os registros
                if releases: # Confirma se foi encontrada a venda
                    cart = [] # Cria um carrinho vazio
                    for release in releases: # Separa as vendas em linhas
                        cart.append({ # Adiciona ao carrinho os produtos
                            "nome": release.nome,
                            "quant": release.quantidade,
                            "valor": release.valor_produto
                        }) 
                        # ============== Dados da venda em si
                        date = release.data # Data da venda
                        client = release.cliente # Nome do Cliente
                        total = release.valor # Valor da Venda
                        payment = release.pagamento # Tipo de Pagamento
                        employee = release.atendente # Atendente

                    # Retorna a criação da Inoice (NNF)
                    return self.create_invoice_archive(
                        store_name = store.nome_loja, cnpj = store.cpf_cnpj, # Nome da Loja
                        address = Store.get_endereco(cr), tel = store.telefone, # Endereço da mesma
                        employye = employee, id_sale = id_venda, # matricula do funcionario e id da venda
                        date = date.strftime('%d/%m/%Y %H:%M'), # Data da venda formata DD/MM/YYYY
                        client = client, cart = cart, total = total, # Nome do cliente,  carrinho sendo composto por um DICt{"nome": prod1, "valor", 0, "quant": 0}
                        payment = payment, cr = cr ), 200 # Retorna Sucesso
                return jsonify("Venda não encontrada"), 404 # Retorna NOT FOUND - 404
            return jsonify("Loja não encontrada!"), 404 # Retorna NOT FOUND - 404
        return jsonify("Id da venda obrigatório!"), 400 # Retorna BAD REQUEST - 400
