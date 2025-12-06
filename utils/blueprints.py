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

from general.routes.email_routes import email_bp
from general.routes.store_routes import store_bp
from general.routes.files_routes import files_bp

from bks.routes.schedule_routes import schedule_bp

from analytics.routes.users_routes import user_bp 
from analytics.routes.analytics_routes import analytics_bp 
from analytics.routes.clients_routes import  clients_bp

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

    # Geral
    store_bp: "/api/lojas",
    email_bp: "/api/email",
    files_bp: "/api/files",

    # BKS
    schedule_bp: "/api/bks/",

    # Analytics
    analytics_bp: "/api/analytics",
    clients_bp: "/api/analytics/clients",
    user_bp: "/api/analytics/users",
}