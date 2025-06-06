from src.Infrastructure.Models.sale import Sale as SaleModel
from src.Infrastructure.Models.product import Product as ProductModel
from src.Config.data_base import db
from src.Domain.sale import Sale as SaleDomain
from datetime import datetime

def create_sale(seller_id, product_id, quantidade):
    product = ProductModel.query.filter_by(id=product_id, seller_id=seller_id).first()
    if not product:
        raise ValueError("Produto não encontrado ou não pertence ao vendedor.")

    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    if not product.status:
        raise ValueError("Produto inativo. Não pode ser vendido.")

    if product.quantidade < quantidade:
        raise ValueError("Estoque insuficiente.")

    nova_venda = SaleModel(
        product_id=product.id,
        seller_id=seller_id,
        quantidade_vendida=quantidade,
        preco_unitario=product.preco,
        data=datetime.utcnow()
    )

    product.quantidade -= quantidade

    db.session.add(nova_venda)
    db.session.commit()

    return nova_venda.to_domain(), product.name
