from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Application.Service import sale_service

class SaleController:
    @staticmethod
    @jwt_required()
    def create_sale():
        data = request.get_json()
        product_id = data.get('produtoId')
        quantidade = data.get('quantidade')

        if not all([product_id, quantidade]):
            return make_response(jsonify({"erro": "Produto e quantidade são obrigatórios."}), 400)

        seller_id = get_jwt_identity()

        try:
            venda = sale_service.create_sale(seller_id, product_id, quantidade)
            return make_response(jsonify(venda.to_dict()), 201)
        except ValueError as ve:
            return make_response(jsonify({"erro": str(ve)}), 400)
        except Exception as e:
            print(f"Erro ao realizar venda: {e}")
            return make_response(jsonify({"erro": "Erro interno ao processar a venda."}), 500)
