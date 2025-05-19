class Sale:
    def __init__(self, id=None, product_id=None, seller_id=None, quantidade_vendida=None, preco_unitario=None, data=None):
        self.id = id
        self.product_id = product_id
        self.seller_id = seller_id
        self.quantidade_vendida = quantidade_vendida
        self.preco_unitario = preco_unitario
        self.data = data

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "seller_id": self.seller_id,
            "quantidade_vendida": self.quantidade_vendida,
            "preco_unitario": self.preco_unitario,
            "data": self.data.isoformat() if self.data else None
        }
