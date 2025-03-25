from src.Infrastructure.Models.user import Seller
from src.Config.data_base import db
from werkzeug.security import generate_password_hash, check_password_hash
import random


class SellerService:
	@staticmethod
    def authenticate(email, password):
        seller = Seller.query.filter_by(email=email).first()
        if seller and check_password_hash(seller.password, password):
            return seller
        return None
