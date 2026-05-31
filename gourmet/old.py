# ======================================================================================
# ======================================================================================
# GOURMET API V1 - ROUTES ==============================================================
# ======================================================================================
# ======================================================================================

api_gourmet = '/gourmet/api/v1/'
gm, rq, socketio, app = []

@app.route(api_gourmet + 'login', methods=['POST'])
def login_gourmet():
    res = gm.login(rq.headers)
    return res

@app.route(api_gourmet + 'caixa', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def gourmet_caixa():
    match rq.method:
        case'POST': res = gm.abrir_caixa(rq.headers, rq.get_json())
        case'GET': res = gm.conferir_caixa(rq.headers.get('cr'))
        case'PATCH': res = gm.aplicar_caixa(rq.get_json(), rq.headers)
        case'DELETE': res = gm.fechar_caixa(rq.headers)
    return res

@app.route(api_gourmet + 'last_value', methods=['POST'])
def gourmet_last_valye():
    res = gm.last_value(rq.headers)
    return res

@app.route(api_gourmet + 'pedidos', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def gourmet_pedidos():
    match rq.method:
        case 'GET': res = gm.get_orders(rq.headers.get('cr'))
        case 'POST': res = gm.new_order(rq.get_json(), rq.headers)
        case 'DELETE': res = gm.rm_order(rq.get_json(), rq.headers)
        case 'PATCH': res = gm.set_leave_order(rq.headers, rq.get_json())
    if rq.method != 'GET' and res[1] == 200: 
        socketio.emit('action', 'pedido')
        socketio.emit('action', 'comanda')
    return res

@app.route(api_gourmet + 'pedido', methods=['DELETE'])
def gourmet_pedido():
    match rq.method:
        case 'DELETE': 
            res = gm.rm_order_with_id(rq.get_json(), rq.headers)
            if res[1] == 200: 
                socketio.emit('action', 'pedido')
                socketio.emit('action', 'comanda')
    return res

@app.route(api_gourmet + 'rm_order_only', methods=['DELETE'])
def gourmet_rm_order():
    res = gm.rm_order_only(rq.headers, rq.get_json())
    if res[1] == 200: 
        socketio.emit('action', 'pedido')
        socketio.emit('action', 'comanda')
    return res

@app.route(api_gourmet + 'prods_pedidos', methods=['POST'])
def gourmet_prods_pedidos():
    res = gm.prods_pedidos(rq.get_json(), rq.headers.get("cr"))
    return res

@app.route(api_gourmet + 'comandas', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def gourmet_comandas():
    match rq.method:
        case 'GET': res = gm.get_cmds(rq.headers.get('cr'))
        case 'POST': res = gm.close_cmd(rq.get_json(), rq.headers)
        case 'DELETE': res = gm.rm_cmd(rq.get_json(), rq.headers)
    if rq.method != 'GET' and res[1] == 200: 
        socketio.emit('action', 'pedido')
        socketio.emit('action', 'comanda')
    return res

@app.route(api_gourmet + 'get_cmd', methods=['POST'])
def gourmet_get_cmd():
    res = gm.get_cmd(rq.headers, rq.get_json())
    return res

@app.route(api_gourmet + 'despesas', methods=['GET', 'POST', 'DELETE'])
def gourmet_despesas():
    mt = rq.method
    if mt == 'POST': res = gm.adicionar_despesas(rq.get_json(), rq.headers)
    if mt == 'GET': res = gm.get_despesas(rq.headers.get('cr'), rq.headers.get('gc'))
    if mt == 'DELETE': res = gm.remover_despesas(rq.args, rq.headers)
    return res

@app.route(api_gourmet + 'produtos', methods=['GET', 'POST', 'PATCH', 'DELETE', 'PUT'])
def gourmet_produtos():
    match rq.method:
        case 'GET': res = gm.consultar_produtos(rq.headers)
        case 'POST': res = gm.add_new_prod(rq.form, rq.headers, rq.files)
        case 'PATCH': res = gm.alter_prod(rq.form, rq.headers, rq.files)
        case 'PUT': res = gm.put_prod(rq.get_json(), rq.headers)
        case 'DELETE': res = gm.rm_prod(rq.get_json(), rq.headers)
    return res

@app.route(api_gourmet + 'combos', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def gourmet_combos():
    match rq.method:
        case 'GET': res = gm.get_combos(rq.args, rq.headers)
        case 'POST': res = gm.set_combo(rq.form, rq.headers, rq.files)
        case 'PATCH': res = gm.update_combo(rq.form, rq.headers, rq.files)
        case 'DELETE': res = gm.remove_combo(rq.get_json(), rq.headers)
    return res

@app.route(api_gourmet + 'add_prod', methods=['POST'])
def gourmet_add_prod():
    res = gm.add_prod(rq.get_json())
    return res

@app.route(api_gourmet + 'rmv_prod', methods=['POST'])
def gourmet_rmv_prod():
    res = gm.rmv_prod(rq.get_json())
    return res

@app.route(api_gourmet + 'vendas', methods=['GET','POST','DELETE','PATCH'])
def gourmet_vendas():
    match rq.method:
        case 'GET': res = gm.get_vendas(rq.headers)
        case 'POST': 
            res = gm.set_venda(rq.get_json(), rq.headers)
            if(res[1] == 200): socketio.emit('action', 'venda')
        case 'DELETE': 
            res = gm.rm_venda(rq.get_json(), rq.headers) 
            if(res[1] == 200): socketio.emit('action', 'venda')
    return res

@app.route(api_gourmet + 'saida', methods=['GET','POST','DELETE','PATCH'])
def gourmet_saida():
    match rq.method:
        case 'GET': res = gm.get_saida(rq.args, rq.headers)
    return res

@app.route(api_gourmet + 'categorias', methods=['GET','POST','DELETE','PATCH'])
def gourmet_categorias():
    match rq.method:
        case 'GET': res = gm.get_categories(rq.headers)
        case 'POST': res = gm.add_categories(rq.get_json(), rq.headers)
        case 'PATCH': res = gm.update_categories(rq.get_json(), rq.headers)
        case 'DELETE': res = gm.rm_categories(rq.get_json(), rq.headers) 
    return res

@app.route(api_gourmet + 'config', methods=['GET','POST','DELETE','PATCH'])
def gourmet_config():
    match rq.method:
        case 'GET': res = gm.get_config_ext(rq.headers)
        case 'POST': res = gm.update_config(rq.get_json(), rq.headers)
    return res

@app.route(api_gourmet + 'funcionarios', methods=['GET','POST','DELETE','PATCH'])
def gourmet_employees():
    match rq.method:
        case 'GET': res = gm.get_employees(rq.headers)
        case 'POST': res = gm.create_employee(rq.form, rq.headers)
        case 'PATCH': res = gm.update_perm_employee(rq.get_json(), rq.headers)
        case 'DELETE': res = gm.delete_employee(rq.get_json(), rq.headers)
    return res

@app.route(api_gourmet + 'relatorios', methods=['POST'])
def gourmet_relatorios():
    res = gm.get_info(rq.get_json(), rq.headers)
    return res

@app.route(api_gourmet + 'rl_vendas', methods=['POST'])
def gourmet_get_vendas_mes():
    res = gm.get_rl_vendas(rq.get_json(), rq.headers)
    return res

@app.route(api_gourmet + 'get_loja/<cr>')
def get_loja(cr):
    return gm.get_dados_loja(cr)