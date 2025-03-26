from src.Config.data_base import db
from src.Domain.user import SellerDomain


class Seller(db.Model):
    tablename = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), default="Inativo")
    activation_code = db.Column(db.String(4), nullable=True)
    role = db.Column(db.String(10), nullable=False, default="Vendedor")

    def to_domain(self):
        return SellerDomain(
            id=self.id,
            name=self.name,
            cnpj=self.cnpj,
            email=self.email,
            phone=self.phone,
            password=self.password,
            status=self.status,
            activation_code=self.activation_code,
            role=self.role
        )
