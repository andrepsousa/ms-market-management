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
            venda, nome_produto = sale_service.create_sale(seller_id, product_id, quantidade)

            resposta = {
                "id": venda.id,
                "product_id": venda.product_id,
                "product_name": nome_produto,
                "seller_id": venda.seller_id,
                "quantidade_vendida": venda.quantidade_vendida,
                "preco_unitario": venda.preco_unitario,
                "data": venda.data.strftime("%d/%m/%Y %H:%M")
            }

            return make_response(jsonify(resposta), 201)

        except ValueError as ve:
            return make_response(jsonify({"erro": str(ve)}), 400)
        except Exception as e:
            print(f"Erro ao realizar venda: {e}")
            return make_response(jsonify({"erro": "Erro interno ao processar a venda."}), 500)
