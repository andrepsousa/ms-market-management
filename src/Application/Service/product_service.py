from src.Infrastructure.Models.product import Product as ProductModel
from src.Config.data_base import db
from src.Domain.product import Product as ProductDomain

def create_product(product: ProductDomain):
    product_model = ProductModel(
        name=product.name,
        preco=product.preco,
        quantidade=product.quantidade,
        status=product.status,
        imagem_url=product.imagem_url,
        seller_id=product.seller_id
    )
    db.session.add(product_model)
    db.session.commit()
    return product_model.to_domain()

def get_product_by_id(product_id, seller_id):
    product = ProductModel.query.filter_by(id=product_id, seller_id=seller_id).first()
    if not product:
        return None
    return product.to_domain()

def list_products_by_seller(seller_id):
    products = ProductModel.query.filter_by(seller_id=seller_id, status=True).all()
    return [product.to_domain() for product in products]

def update_product(product_id, seller_id, updated_product: ProductDomain):
    product_model = ProductModel.query.filter_by(id=product_id, seller_id=seller_id).first()
    if not product_model:
        return None

    product_model.update_from_domain(updated_product)
    db.session.commit()
    return product_model.to_domain()

def inactivate_product(product_id, seller_id):
    product_model = ProductModel.query.filter_by(id=product_id, seller_id=seller_id).first()
    if not product_model:
        return None

    product_model.status = False
    db.session.commit()
    return product_model.to_domain()

def activate_product(product_id, seller_id):
    product_model = ProductModel.query.filter_by(id=product_id, seller_id=seller_id).first()
    if not product_model:
        return None
    
    product_model.status = True
    db.session.commit()
    return product_model.to_domain()

