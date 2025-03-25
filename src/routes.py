from flask import Blueprint, jsonify, make_response
from src.Application.Controllers.user_controller import (
    LoginController, SellerController
)


main_bp = Blueprint("main_bp", __name__)


@main_bp.route('/api/auth/login', methods=['POST'])
def login():
    return LoginController.login()
