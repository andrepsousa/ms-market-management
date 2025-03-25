from flask import request, jsonify, make_response
from src.Application.Service.user_service import SellerService
from src.Infrastructure.Models.user import Seller


class SellerController:
    @staticmethod
    def register_seller():
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        status = data.get('status', 'Inativo')
        activation_code = data.get('activation_code')

        if not all([name, cnpj, email, phone, password, activation_code]):
            return make_response(jsonify({
                "erro": "Todos os campos são obrigatórios."
            }), 400)

        if Seller.query.filter_by(email=email).first():
            return make_response(jsonify({
                "erro": "Email já em uso."
            }), 400)

        seller = SellerService.create_user(
            name, cnpj, email, phone, password, status)
        return make_response(jsonify({
            "mensagem": "Vendedor salvo com sucesso!",
            "seller": seller.to_dict()
        }), 201)

    @staticmethod
    def get_sellers():
        users = SellerService.get_seller()
        return make_response(jsonify([user.to_dict() for user in users]), 200)

    @staticmethod
    def get_seller_id(seller_id):
        user = SellerService.get_seller_by_id(seller_id)
        if not user:
            return make_response(jsonify({
                "erro": "Usuário não encontrado."
            }), 404)
        return make_response(jsonify(user.to_dict()), 200)

    @staticmethod
    def update_sellers(seller_id):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        status = data.get('status')
        activation_code = data.get('activation_code')

        user = SellerService.update_seller(
            seller_id, name, email, phone, password, status, activation_code
        )
        if not user:
            return make_response(jsonify({
                "error": "Usuário não encontrado."
            }), 404)
        return make_response(jsonify(user.to_dict()), 200)

    @staticmethod
    def delete_sellers(seller_id):
        seller = SellerService.delete_seller(seller_id)
        if not seller:
            return make_response(jsonify({
                "error": "Usuário não encontrado."
            }), 404)
        return make_response(jsonify({"message": "Usuário deletado!"}), 200)


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
