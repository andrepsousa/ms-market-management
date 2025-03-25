from flask import Blueprint, jsonify, make_response
from src.Application.Controllers.user_controller import (
    LoginController, SellerController
)


main_bp = Blueprint("main_bp", __name__)


@main_bp.route('/api', methods=['GET'])
def health():
    return make_response(jsonify({
        "mensagem": "API - OK; Docker - Up",
    }), 200)


@main_bp.route('/api/sellers', methods=['POST'])
def create_sellers():
    return SellerController.register_seller()


@main_bp.route('/api/sellers', methods=['GET'])
def list_sellers():
    return SellerController.get_sellers()


@main_bp.route('/api/sellers/<int:seller_id>', methods=['GET'])
def get_sellers_by_id(seller_id):
    return SellerController.get_seller_id(seller_id)


@main_bp.route('/api/sellers/<int:seller_id>/update', methods=['PUT'])
def put_seller(seller_id):
    return SellerController.update_sellers(seller_id)


@main_bp.route('/api/sellers/<int:seller_id>/delete', methods=['DELETE'])
def remove_sellers(seller_id):
    return SellerController.delete_sellers(seller_id)


@main_bp.route('/api/auth/login', methods=['POST'])
def login():
    return LoginController.login()