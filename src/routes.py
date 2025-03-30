from flask import Blueprint, jsonify, make_response
from src.Application.Controllers.user_controller import (
    LoginController, SellerController
)
from flask_jwt_extended import jwt_required


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
@jwt_required()
def list_sellers():
    return SellerController.get_sellers()


@main_bp.route('/api/sellers/<int:seller_id>', methods=['GET'])
@jwt_required()
def get_sellers_by_id(seller_id):
    return SellerController.get_seller_id(seller_id)


@main_bp.route('/api/sellers/<int:seller_id>/update', methods=['PUT'])
@jwt_required()
def put_seller(seller_id):
    return SellerController.update_sellers(seller_id)


@main_bp.route('/api/sellers/<int:seller_id>/delete', methods=['DELETE'])
@jwt_required()
def remove_sellers(seller_id):
    return SellerController.delete_sellers(seller_id)

@main_bp.route('/api/sellers/<int:seller_id>/activate/<activation_code>', methods=['POST'])
def activate_seller(seller_id, activation_code):
    return SellerController.activate_seller(seller_id, activation_code)    

@main_bp.route('/api/auth/login', methods=['POST'])
def login():
    return LoginController.login()