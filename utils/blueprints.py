from manager.routes.clients_routes import clientes_bp
from manager.routes.employees_routes import employees_bp
from manager.routes.config_routes import config_bp
from manager.routes.products_routes import product_bp
from manager.routes.orders_routes import os_bp
from manager.routes.brand_routes import brand_bp
from manager.routes.pos_routes import pos_bp
from manager.routes.config_routes import config_bp
from manager.routes.sales_routes import sales_bp
from manager.routes.releases_routes import release_bp
from manager.routes.invoice_route import invoice_bp
from bks.routes.schedule_routes import schedule_bp

blueprints = {
    clientes_bp: "/api/manager/clientes",
    employees_bp: "/api/manager/funcionarios",
    config_bp: "/api/manager/config",
    product_bp: "/api/manager/produtos",
    os_bp: "/api/manager/os",
    brand_bp: "/api/manager/marcas",
    pos_bp: "/api/manager/caixa",
    config_bp: "/api/manager/config",
    sales_bp: "/api/manager/vendas",
    invoice_bp: "/api/manager/nnf",
    release_bp: "/api/manager/saidas",
    schedule_bp: "/api/bks/",
}