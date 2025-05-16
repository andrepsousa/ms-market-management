from src.Config.data_base import db

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, default=True)
    imagem_url = db.Column(db.String(255))
    seller_id = db.Column(db.Integer, nullable=False)

    def to_domain(self):
        from src.Domain.product import Product as ProductDomain
        return ProductDomain(
            id=self.id,
            name=self.name,
            preco=self.preco,
            quantidade=self.quantidade,
            status=self.status,
            imagem_url=self.imagem_url,
            seller_id=self.seller_id
        )

    def update_from_domain(self, domain_product):
        self.name = domain_product.name
        self.preco = domain_product.preco
        self.quantidade = domain_product.quantidade
        self.status = domain_product.status
        self.imagem_url = domain_product.imagem_url
