# BPS Manager =============================================
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
from manager.routes.reports_routes import reports_bp
from manager.routes.parts_routes import parts_bp
from manager.routes.expenses_routes import expenses_bp
from manager.routes.providers_routes import providers_bp
from manager.routes.categories_routes import categories_bp

# BPS Gourmet =============================================
from gourmet.routes.auth_routes import auth_bp as auth_gourmet_bp
from gourmet.routes.pos_routes import pos_bp as pos_gourmet_bp
from gourmet.routes.products_routes import products_bp as products_gourmet_bp
from gourmet.routes.categories_routes import categories_bp as categories_gourmet_bp

# BPS Gerais =============================================
from general.routes.email_routes import email_bp
from general.routes.store_routes import store_bp
from general.routes.files_routes import files_bp

# BPS BKSchedular =============================================
from bks.routes.schedule_routes import schedule_bp

blueprints = {
    # Manager
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
    reports_bp: "/api/manager/dashboards",
    parts_bp: "/api/manager/pecas",
    expenses_bp: "/api/manager/despesas",
    providers_bp: "/api/manager/fornecedores",
    categories_bp: "/api/manager/categorias",

    # Geral
    store_bp: "/api/lojas",
    email_bp: "/api/email",
    files_bp: "/api/files",

    # BKSchedular
    schedule_bp: "/api/bks",

    # Gourmet
    auth_gourmet_bp: "/api/gourmet/auth",
    pos_gourmet_bp: "/api/gourmet/caixa",
    products_gourmet_bp: "/api/gourmet/produtos",
    categories_gourmet_bp: "/api/gourmet/categorias",
}