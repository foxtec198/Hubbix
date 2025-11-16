from manager.routes.clients_routes import clientes_bp
from manager.routes.employees_routes import employees_bp
from manager.routes.config_routes import config_bp
from manager.routes.products_routes import product_bp
from manager.routes.service_order_routes import os_bp

blueprints = {
    clientes_bp: "/api/manager/clientes",
    employees_bp: "/api/manager/funcionarios",
    config_bp: "/api/manager/config",
    product_bp: "/api/manager/produtos",
    os_bp: "/api/manager/os",
}