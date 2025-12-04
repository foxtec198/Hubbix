from PIL import Image, ImageDraw, ImageFont
from utils.to_real import to_real
from os import getcwd, path
from models.store_model import Store
from utils.safe_route import check_connection, require_cr
from werkzeug.datastructures import Headers, MultiDict
from utils.db import cons

# Fontes
coolvetica = path.join(getcwd(), "manager", "assets", "fonts", "coolvetica.otf")
bebas = path.join(getcwd(), "manager", "assets", "fonts", "BebasNeue-Regular.ttf")
Astonpoliz = path.join(getcwd(), "manager", "assets", "fonts", "Astonpoliz.otf")

class InvoiceService: # Back end das notas fiscais
    def __init__(self): # Define a altura e largura inicial
        self.font = ImageFont.truetype(Astonpoliz, 10)
        self.largura = 380
        self.altura = 380

    @check_connection
    @require_cr
    def create(self, id:MultiDict, hd:Headers, cr = None): # Cria a nota pelo ROUTE
        id_venda = bd.get('id_venda')
        store = Store.query.filter_by(cr=cr).one()
        releases = cons(
            """
                select distinct s.nome, count(s.nome) as quant, s.valor, v.data, c.nome, v.valor, v.pagamento, f.nome
                from saidas s
                inner join vendas v on v.id = s.id_venda
                inner join clientes c on c.id = v.id_cliente
                inner join funcionarios f on f.matricula = v.matricula
                where v.id = %s
                and v.cr = '%s'
                GROUP BY s.nome, s.valor, v.data, c.nome, v.valor, v.pagamento, f.nome
            """, (id_venda, cr), all=True
        )

        cart = []
        total = 0
        for release in releases:
            cart.append({
                "nome": release[0],
                "quant": release[1],
                "valor": release[2]
            })
            data = release[3]
            cliente = release[4]
            total += release[5]
            pag = release[6]
            atendente = release[7]

        return self.create_invoice_archive(
            storeName = store.nome_loja,
            cnpj = store.cpf_cnpj,
            address = Store.get_endereco(cr),
            tel = store.telefone,
            func = atendente,
            numSell = id_venda,
            date = data.strftime('%d/%m/%Y %H:%M'),
            client = cliente,
            cart = cart,
            total = total,
            mtpg = pag,
            cr = cr
        )

    def get_x(self, texto): # Centraliza o texto
        texto = str(texto)
        bbox = self.draw.textbbox((0, 0), texto, font= self.font)
        return (self.largura - (bbox[2] - bbox[0])) // 2

    def draw_text(self, x, y, texto, font=None): # Escreve o texto na img
        font = self.font if not font else font
        self.draw.text((x, y), texto, font=font, fill=(0, 0, 0))

    def separador(self, y, key='='): # Apenas separa com algum caractere
        separador = key * self.largura
        self.draw_text(self.get_x(separador), y, separador)
    
    def separador_with_text(self, y, text:str): # Separa com texto no meio
        txtl = len(text)
        total = self.largura + txtl
        meio = (total - txtl ) // 2

        separador = '=' * meio + f" {text} " + '=' * meio
        self.draw_text(self.get_x(separador), y, separador)
            
    def create_invoice_archive(self, storeName, cnpj, address, tel, func, numSell, date, client, cart, total, mtpg, cr): # Cria o arquivo da nota
        # Dependendo do tamamho do carrinho modifica o tamnho do doc
        if cart:
            for i in range(1, len(cart) + 1):
                self.altura += 25
                    
        self.img = Image.new("RGB", (self.largura, self.altura), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)

        # Carrega as fontes
        fontTitulo = ImageFont.truetype(bebas, 18)
        fontSub = ImageFont.truetype(coolvetica, 11)

        # ----------------------CABEÇALHO----------------------------
        # Titulo 
        self.draw_text(self.get_x(storeName), 15, storeName, fontTitulo)

        # CNPJ ou CPF
        self.draw_text(20, 40, f"CNPJ: {cnpj}")

        # Endereço
        self.draw_text(20, 60, f"Endereço: {address}")

        # Telefone
        self.draw_text(20, 80, f"Telefone: {tel}")

        # Funcionario
        self.draw_text(20, 100, f"Atendente: {func}")

        # Numero de Venda
        nSell = f"Venda N°{numSell}"
        self.separador(120)
        self.draw_text(self.get_x(nSell), 130, nSell)
        self.separador(140)

        # ------------------------CORPO------------------------------

        # Data da Compra
        self.draw_text(20, 160, f"Data e Hora: {date}")

        # Nome do Cliente
        self.draw_text(20, 180, f"Cliente: {client}")

        self.separador_with_text(200, 'PRODUTOS')
        self.draw_text(20, 220, "Item") 
        self.draw_text(230, 220, "Qtd.")
        self.draw_text(280, 220, "Vlr.")
        self.draw_text(330, 220, "Subtotal")
        self.separador(230, '-')

        y = 240
        for item in cart:
            print(item)
            self.draw_text(20, y, item['nome'])
            self.draw_text(230, y, str(item['quant']))
            self.draw_text(280, y, to_real(item['valor']))
            self.draw_text(330, y, to_real(item['valor'] * item['quant']))
            y += 20

        self.separador_with_text(y, "PAGAMENTO")

        ttll = "Total da Venda"
        self.draw_text(self.get_x(ttll), y + 20, ttll)
        self.draw_text(330, y + 20, to_real(total)) # Total em float

        mtlbl = 'Metodo de Pagamento'
        self.draw_text(self.get_x(mtlbl), y + 40, mtlbl)

        # Metodo de Pagamento
        self.draw_text(330, y + 40, mtpg)
        
        self.separador(y + 50, "-")

        # ------------------------FOOTER------------------------------

        aviso = "*** Esse ticket não é documento fiscal ***"
        self.draw_text(self.get_x(aviso), y + 60, aviso)

        agradecimento = "OBRIGADO E VOLTE SEMPRE!"
        self.draw_text(self.get_x(agradecimento), y + 80, agradecimento, fontSub)

        self.separador(y + 100, "-")

        devby = "Desenvolvido por ®Hubbix Sistemas - hubbix.com.br"
        self.draw_text(20, y + 120, devby)
        
        nome_arquivo = f'{cr}_{numSell}.pdf'
        caminhoImg = path.join(getcwd(), "manager", "assets", "nnfs", nome_arquivo)
        # Salva a imagem (opcional)
        self.img.save(caminhoImg)
        return nome_arquivo
    
    def create_example(self): # Gera um exemplo de nota fiscal
        self.img = Image.new("RGB", (self.largura, self.altura), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)
        # carrega a fonte padrão

        fontTitulo = ImageFont.truetype(bebas, 18)
        fontSub = ImageFont.truetype(coolvetica, 11)

        # Titulo 
        titulo = "Nome da Loja"
        self.draw_text(self.get_x(titulo), 15, titulo, fontTitulo)

        cnpj = 'CNPJ: 00000000000000'
        self.draw_text(20, 40, cnpj)

        endereco = "Nome da Rua 999, Bairro - Cidade UF"
        self.draw_text(20, 60, endereco)

        telefone = "43996617904" 
        self.draw_text(20, 80, telefone)

        funcionario = "Funcionario: Guilherme"
        self.draw_text(20, 100, funcionario)

        self.separador(120)

        venda = "Venda N° 999"
        self.draw_text(self.get_x(venda), 130, venda)

        self.separador(140)

        data = "Data e Hora: 20/05/2022 10:20"
        self.draw_text(20, 160, data)

        cliente = "Cliente: Não Informado"
        self.draw_text(20, 180, cliente)

        self.separador_with_text(
             200, 'PRODUTOS'
        )

        self.draw_text(20, 220, "Item")
        self.draw_text(230, 220, "Qtd.")
        self.draw_text(280, 220, "Vlr.")
        self.draw_text(330, 220, "Subtotal")
        self.separador(230, '-')

        cart = [{
            'nome': 'Produto',
            'quant': 2,
            'valor': 20
        }]

        y = 240
        for item in cart:
            self.draw_text(20, y, item['nome'])
            self.draw_text(230, y, to_real(item['quant']))
            self.draw_text(280, y, to_real(item['valor']))
            self.draw_text(330, y, to_real(item['valor'] * item['quant']))
            y += 20

        self.separador_with_text(y, "PAGAMENTO")
        ttll = "Total da Venda"
        self.draw_text(self.get_x(ttll), y + 20, ttll)
        total = 40
        self.draw_text(330, y + 20, to_real(total))

        mtlbl = 'Metodo de Pagamento'
        self.draw_text(self.get_x(mtlbl), y + 40, mtlbl)

        mtpg = "DEBITO"
        self.draw_text(330, y + 40, mtpg)
        
        self.separador(y + 50, "-")

        aviso = "*** Essa ticket não é documento fiscal ***"
        self.draw_text(self.get_x(aviso), y + 60, aviso)

        agradecimento = "OBRIGADO E VOLTE SEMPRE!"
        self.draw_text(self.get_x(agradecimento), y + 80, agradecimento, fontSub)

        self.separador(y + 100, "-")

        devby = "Desenvolvido por ®Hubbix Sistemas - hubbix.com.br"
        self.draw_text(20, y + 120, devby)

        # Salva a imagem (opcional)
        self.img.save(path.join(getcwd(), "manager", "assets", "nnfs", "exemplo_nota.pdf"))
    

