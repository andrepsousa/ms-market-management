from flask import request, jsonify, make_response
from src.Application.Service.user_service import SellerService
from src.Infrastructure.Models.user import Seller
from src.Infrastructure.http.whats_app import WhatsAppService
from src.Config.data_base import db


class SellerController:
    @staticmethod
    def register_seller():
        # Obter dados da requisição
        data = request.get_json()
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        status = "Inativo"  # O status será "Inativo" inicialmente

        # Verificar se todos os campos obrigatórios foram fornecidos
        if not all([name, cnpj, email, phone, password]):
            return make_response(jsonify({"erro": "Todos os campos são obrigatórios."}), 400)

        # Verificar se o email já está em uso
        if Seller.query.filter_by(email=email).first():
            return make_response(jsonify({"erro": "Email já em uso."}), 400)

        try:
            # Criar o vendedor e gerar o código de ativação
            seller = SellerService.create_user(
                name, cnpj, email, phone, password, status
            )

            return make_response(jsonify({
                "mensagem": "Vendedor salvo com sucesso! Um código de ativação foi enviado via WhatsApp.",
                "seller": seller.to_dict()
            }), 201)

        except Exception as e:
            # Log do erro
            return make_response(jsonify({"erro": "Erro ao registrar o vendedor."}), 500)

    @staticmethod
    def activate_seller(seller_id, activation_code):
        seller = Seller.query.get(seller_id)
        if not seller:
            return make_response(jsonify({"erro": "Vendedor não encontrado."}), 404)
        
        if str(seller.activation_code) == str(activation_code):
            seller.status = "Ativo"
            seller.activation_code = None  # Limpar o código de ativação depois de validado
            db.session.commit()
            return make_response(jsonify({"mensagem": "Vendedor ativado com sucesso!"}), 200)
        
        return make_response(jsonify({"erro": "Código de ativação inválido."}), 400)

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

        user = SellerService.update_seller(
            seller_id, name, email, phone, password
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
