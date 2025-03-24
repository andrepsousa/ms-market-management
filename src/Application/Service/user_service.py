from src.Infrastructure.Models.user import User


class LoginService:
    @staticmethod
    def sign_in(email, password):
        return User.query.filter_by(email=email, password=password).first()
