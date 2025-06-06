from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from src.Application.Service.user_service import SellerService
from src.Infrastructure.Models.user import Seller
from src.Infrastructure.http.whats_app import WhatsAppService
from src.Config.data_base import db
from datetime import timedelta
import re
from werkzeug.security import generate_password_hash, check_password_hash



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

        # Validar formato do email (simples)
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return make_response(jsonify({"erro": "Email inválido."}), 400)

        # Validar o formato do telefone, considerando o formato internacional (+55)
        if not re.match(r'^\+55\d{11}$', phone):
            return make_response(jsonify({"erro": "Telefone inválido. Deve ter 13 dígitos, incluindo o código do país (+55)."}), 400)

        # Validar o tamanho do CNPJ (geralmente 14 dígitos)
        if len(cnpj) != 14 or not cnpj.isdigit():
            return make_response(jsonify({"erro": "CNPJ inválido. Deve ter exatamente 14 dígitos."}), 400)

        # Verificar se o email já está em uso
        if Seller.query.filter_by(email=email).first():
            return make_response(jsonify({"erro": "Email já em uso."}), 400)
        
        # Verificar se o CNPJ já está em uso
        if Seller.query.filter_by(cnpj=cnpj).first():
            return make_response(jsonify({"erro": "CNPJ já cadastrado."}), 400)


        try:
            # Criar o vendedor e gerar o código de ativação
            seller = SellerService.create_user(name, cnpj, email, phone, password, status)

            return make_response(jsonify({
                "mensagem": "Vendedor salvo com sucesso! Um código de ativação foi enviado via WhatsApp.",
                "seller": seller.to_dict()
            }), 201)

        except Exception as e:
            print(f"Erro: {str(e)}")  # Para debugging, pode remover em produção
            return make_response(jsonify({"erro": "Erro ao registrar o vendedor."}), 500)
        
    @staticmethod
    def activate_seller(phone, activation_code):
        seller = Seller.query.filter_by(phone=phone).first()
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
            return make_response(jsonify({"erro": "Usuário não encontrado."}), 404)
        return make_response(jsonify(user.to_dict()), 200)

    @staticmethod
    def update_sellers(seller_id):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        # Verificação de campos obrigatórios
        if not name:
            return make_response(jsonify({"error": "O nome não pode estar vazio."}), 400)
        
        if not email:
            return make_response(jsonify({"error": "O e-mail não pode estar vazio."}), 400)

        if not phone:
            return make_response(jsonify({"error": "O telefone não pode estar vazio."}), 400)

        # Validação de e-mail
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            return make_response(jsonify({"error": "E-mail inválido."}), 400)
        
         # Validação do telefone (somente números e exatamente 13 dígitos)
        phone_regex = r'^\+55\d{11}$'
        if not re.match(phone_regex, phone):
            return make_response(jsonify({"error": "O telefone deve estar no formato correto: +55XXXXXXXXXXX"}), 400)

        user = SellerService.get_seller_by_id(seller_id)
        if not user:
                return make_response(jsonify({"error": "Usuário não encontrado."}), 404)

        # Criptografar a senha apenas se ela for diferente da atual
        if password and not check_password_hash(user.password, password):
            password = generate_password_hash(password, method='pbkdf2:sha256')
        else:
            password = user.password  # Mantém a senha antiga



        # Buscar usuário para verificações adicionais
        user = SellerService.get_seller_by_id(seller_id)
        if not user:
            return make_response(jsonify({"error": "Usuário não encontrado."}), 404)

        # Verificar se a senha nova é a mesma que a atual
        if password and user.password == password:
            return make_response(jsonify({"error": "A nova senha não pode ser igual à senha atual."}), 400)

        updated_user = SellerService.update_seller(seller_id, name, email, phone, password)
        return make_response(jsonify(updated_user.to_dict()), 200)




    @staticmethod
    def delete_sellers(seller_id):
        seller = SellerService.delete_seller(seller_id)
        if not seller:
            return make_response(jsonify({"error": "Usuário não encontrado."}), 404)
        return make_response(jsonify({"message": "Usuário deletado!"}), 200)


class LoginController:
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        seller = SellerService.authenticate(email, password)

        if seller and seller.status == "Ativo":
            access_token = create_access_token(identity=str(seller.id), expires_delta=timedelta(hours=1))
            return make_response(jsonify({
                "message": "Login realizado com sucesso!",
                "access_token": access_token,
                "user": seller.to_domain().to_dict()
            }), 200)
        elif seller and seller.status == "Inativo":
            try:
                # Enviar código de ativação via WhatsApp
                whatsapp_service = WhatsAppService()
                activation_code = seller.activation_code
                whatsapp_service.enviar_codigo(seller.phone, activation_code)
            except Exception as e:
                return make_response(jsonify({"error": "Erro ao enviar o código de ativação via WhatsApp."}), 500)
            return make_response(jsonify({"error": "Vendedor inativo. Verifique o código enviado para o seu WhatsApp."}), 403)

        if not seller:
            return make_response(jsonify({"error": "Email ou senha inválidos."}), 401)

        return make_response(jsonify({"error": "Erro ao autenticar o vendedor."}), 500)
