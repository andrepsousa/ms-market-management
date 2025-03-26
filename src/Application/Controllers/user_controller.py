from flask import request, jsonify, make_response
from src.Application.Service.user_service import SellerService
from src.Infrastructure.Models.user import Seller
from src.Infrastructure.http.whats_app import WhatsAppService



class SellerController:
    @staticmethod
    def register_seller():
        # Obter dados da requisição
        data = request.get_json()
        print("Dados recebidos:", data)  # Exibe os dados recebidos na requisição
        name = data.get('name')
        cnpj = data.get('cnpj')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        status = "Inativo"  # O status será "Inativo" inicialmente

        # Verificar se todos os campos obrigatórios foram fornecidos
        if not all([name, cnpj, email, phone, password]):
            print("Erro: Faltam campos obrigatórios!")  # Log de erro caso falte algum campo
            return make_response(jsonify({"erro": "Todos os campos são obrigatórios."}), 400)

        # Verificar se o email já está em uso
        if Seller.query.filter_by(email=email).first():
            print(f"Erro: Email já em uso: {email}")  # Log se o email já estiver em uso
            return make_response(jsonify({"erro": "Email já em uso."}), 400)

        try:
            # Criar o vendedor e gerar o código de ativação
            print("Criando vendedor e gerando código de ativação...")  # Log indicando a criação do vendedor
            seller = SellerService.create_user(
                name, cnpj, email, phone, password, status
            )

            # Criar o serviço de WhatsApp apenas se for necessário
            if seller.activation_code:
                print(f"Enviando código de ativação para o número: {phone}")  # Log antes de enviar o código
                account_sid = "your_account_sid"
                auth_token = "your_auth_token"
                twilio_number = "your_twilio_number"
                
                whats_app_service = WhatsAppService(
                    account_sid=account_sid,
                    auth_token=auth_token,
                    twilio_number=twilio_number
                )
                response = whats_app_service.enviar_codigo(phone, seller.activation_code)  # Envia o código
                print(f"Resposta do serviço WhatsApp: {response}")  # Log da resposta do serviço

            print("Vendedor criado com sucesso!")  # Log de sucesso após criar o vendedor
            return make_response(jsonify({
                "mensagem": "Vendedor salvo com sucesso! Um código de ativação foi enviado via WhatsApp.",
                "seller": seller.to_dict()
            }), 201)

        except Exception as e:
            # Log do erro
            print(f"Erro ao registrar vendedor: {e}")
            return make_response(jsonify({"erro": "Erro ao registrar o vendedor."}), 500)

    @staticmethod
    def activate_seller(seller_id, activation_code):
        seller = Seller.query.get(seller_id)
        if not seller:
            return make_response(jsonify({"erro": "Vendedor não encontrado."}), 404)
        
        if seller.activation_code == activation_code:
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
