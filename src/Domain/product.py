class Product:
    def __init__(self, id=None, name=None, preco=None, quantidade=None, status=True, imagem_url=None, seller_id=None):
        self.id = id
        self.name = name
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.imagem_url = imagem_url
        self.seller_id = seller_id

    def inactivate(self):
        self.status = False
    
    def activate(self):
        self.status = True

    def is_active(self):
        return self.status

    def update(self, name=None, preco=None, quantidade=None, imagem_url=None):
        if name: self.name = name
        if preco: self.preco = preco
        if quantidade: self.quantidade = quantidade
        if imagem_url: self.imagem_url = imagem_url

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "imagem_url": self.imagem_url,
            "seller_id": self.seller_id
        }
