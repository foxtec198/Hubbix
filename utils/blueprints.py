from manager.routes.clients_routes import clientes_bp
from manager.routes.employees_routes import employees_bp
from manager.routes.config_routes import config_bp
from manager.routes.products_routes import product_bp
from manager.routes.service_order_routes import os_bp
from manager.routes.brand_routes import brand_bp
from manager.routes.cash_register_routes import cr_bp

from bks.routes.schedule_routes import schedule_bp

blueprints = {
    clientes_bp: "/api/manager/clientes",
    employees_bp: "/api/manager/funcionarios",
    config_bp: "/api/manager/config",
    product_bp: "/api/manager/produtos",
    os_bp: "/api/manager/os",
    brand_bp: "/api/manager/marcas",
    cr_bp: "/api/manager/caixa",
    schedule_bp: "/api/bks/",
}