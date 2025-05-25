from flask import Blueprint
from src.Application.Controllers.product_controller import ProductController

product_bp = Blueprint('product_bp', __name__)

# Criar produto
@product_bp.route('/api/products/criar', methods=['POST'])
def create_product():
    return ProductController.create_product()

# Listar produtos do vendedor autenticado
@product_bp.route('/api/products', methods=['GET'])
def list_products():
    return ProductController.list_products()

# Buscar produto por ID
@product_bp.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return ProductController.get_product(product_id)

# Atualizar produto
@product_bp.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return ProductController.update_product(product_id)

# Inativar produto
@product_bp.route('/api/products/<int:product_id>/inactivate', methods=['PATCH'])
def inactivate_product(product_id):
    return ProductController.inactivate_product(product_id)
