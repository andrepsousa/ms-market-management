class SellerDomain:
    def init(self, id, name, cnpj, email, phone, password,
            status="Inativo", activation_code=None, role="Cliente"):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.phone = phone
        self.password = password
        self.status = status
        self.activation_code = activation_code
        self.role = role

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "phone": self.phone,
            "status": self.status,
            "activation_code": self.activation_code,
            "role": self.role
        }
