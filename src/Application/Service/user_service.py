from src.Infrastructure.Models.user import Seller
from src.Infrastructure.http.whats_app import WhatsAppService
from src.Config.data_base import db
from werkzeug.security import generate_password_hash, check_password_hash
import random


class SellerService:
    @staticmethod
    def create_user(name, cnpj, email, phone, password, role="Vendedor"):
        hashed_password = generate_password_hash(password)
        
        activation_code = str(random.randint(1000, 9999))
        print(f'ESse é o Código: {activation_code}')

        new_seller = Seller(
            name=name,
            cnpj=cnpj,
            email=email,
            phone=phone,
            password=hashed_password,
            status="Inativo",
            activation_code=activation_code,
            role="Vendedor"
        )

        db.session.add(new_seller)
        db.session.commit()

        whatsapp_service = WhatsAppService()
        whatsapp_service.enviar_codigo(phone, activation_code)

        return new_seller.to_domain()
  

    @staticmethod
    def get_seller():
        seller = Seller.query.all()
        return [sellers.to_domain() for sellers in seller]

    @staticmethod
    def get_seller_by_id(seller_id):
        seller = Seller.query.get(seller_id)
        return seller.to_domain() if seller else None

    @staticmethod
    def update_seller(seller_id, name, email, phone,
                      password):
        seller = Seller.query.get(seller_id)
        if not seller:
            return None
        seller.name = name
        seller.email = email
        seller.phone = phone
        seller.password = password
        db.session.commit()
        return seller.to_domain()

    @staticmethod
    def delete_seller(seller_id):
        seller = Seller.query.get(seller_id)
        if not seller:
            return None
        db.session.delete(seller)
        db.session.commit()
        return seller.to_domain()

    @staticmethod
    def authenticate(email, password):
        seller = Seller.query.filter_by(email=email).first()
        if seller and check_password_hash(seller.password, password):
            return seller
        return None