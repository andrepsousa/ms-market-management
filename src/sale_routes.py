from flask import Blueprint
from src.Application.Controllers.sale_controller import SaleController

sale_bp = Blueprint('sale_bp', __name__)

@sale_bp.route('/api/sales', methods=['POST'])
def create_sale():
    return SaleController.create_sale()
