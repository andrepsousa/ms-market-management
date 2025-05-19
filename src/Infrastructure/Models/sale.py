from src.Config.data_base import db
from src.Domain.sale import Sale as SaleDomain
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, nullable=False)
    quantidade_vendida = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def to_domain(self):
        return SaleDomain(
            id=self.id,
            product_id=self.product_id,
            seller_id=self.seller_id,
            quantidade_vendida=self.quantidade_vendida,
            preco_unitario=self.preco_unitario,
            data=self.data
        )
