from flask import request, jsonify, make_response
from src.Application.Service.user_service import SellerService
from src.Infrastructure.Models.user import Seller


class LoginController:
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        seller = SellerService.authenticate(email, password)

        if seller:
            return make_response(jsonify({
                "messagem": "Login successful!",
                "user": seller.to_domain().to_dict()
            }), 200)

        else:
            return make_response(jsonify({
                "error": "Invalid credentials"
            }), 400)
