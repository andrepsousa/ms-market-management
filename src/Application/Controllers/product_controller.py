from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service import product_service
from src.Domain.product import Product as ProductDomain

class ProductController:
    @staticmethod
    @jwt_required()
    def create_product():
        data = request.get_json()
        name = data.get('name')
        preco = data.get('preco')
        quantidade = data.get('quantidade')
        imagem_url = data.get('imagem_url')

        if not all([name, preco, quantidade]):
            return make_response(jsonify({"erro": "Nome, preço e quantidade são obrigatórios."}), 400)

        try:
            seller_id = get_jwt_identity()
            product = ProductDomain(
                name=name,
                preco=preco,
                quantidade=quantidade,
                imagem_url=imagem_url,
                status=True,
                seller_id=seller_id
            )
            created_product = product_service.create_product(product)
            return make_response(jsonify(created_product.to_dict()), 201)
        except Exception as e:
            print(f"Erro ao criar produto: {e}")
            return make_response(jsonify({"erro": "Erro interno ao criar produto."}), 500)

    @staticmethod
    @jwt_required()
    def get_product(product_id):
        seller_id = get_jwt_identity()
        product = product_service.get_product_by_id(product_id, seller_id)
        if not product:
            return make_response(jsonify({"erro": "Produto não encontrado."}), 404)
        return make_response(jsonify(product.to_dict()), 200)

    @staticmethod
    @jwt_required()
    def list_products():
        seller_id = get_jwt_identity()
        products = product_service.list_products_by_seller(seller_id)
        return make_response(jsonify([p.to_dict() for p in products]), 200)
    
    @staticmethod
    @jwt_required()
    def list_products_inactivated():
        seller_id = get_jwt_identity()
        products = product_service.list_products_by_seller_inactivated(seller_id)
        return make_response(jsonify([p.to_dict() for p in products]), 200)
    
    @staticmethod
    @jwt_required()
    def update_product(product_id):
        data = request.get_json()
        name = data.get('name')
        preco = data.get('preco')
        quantidade = data.get('quantidade')
        imagem_url = data.get('imagem_url')

        if not all([name, preco, quantidade]):
            return make_response(jsonify({"erro": "Nome, preço e quantidade são obrigatórios."}), 400)

        seller_id = get_jwt_identity()
        updated_product = ProductDomain(
            name=name,
            preco=preco,
            quantidade=quantidade,
            imagem_url=imagem_url,
            status=True,
            seller_id=seller_id
        )
        product = product_service.update_product(product_id, seller_id, updated_product)
        if not product:
            return make_response(jsonify({"erro": "Produto não encontrado para atualização."}), 404)

        return make_response(jsonify(product.to_dict()), 200)

    @staticmethod
    @jwt_required()
    def inactivate_product(product_id):
        seller_id = get_jwt_identity()
        product = product_service.inactivate_product(product_id, seller_id)
        if not product:
            return make_response(jsonify({"erro": "Produto não encontrado para inativação."}), 404)
        return make_response(jsonify({"mensagem": "Produto inativado com sucesso."}), 200)

    @staticmethod
    @jwt_required()
    def activate_product(product_id):
        seller_id = get_jwt_identity()
        product = product_service.activate_product(product_id, seller_id)
        if not product:
            return make_response(jsonify({"erro": "Produto não encontrado para a ativação"}), 404)
        return make_response(jsonify({"erro": "Produto ativado com sucesso"}), 200)