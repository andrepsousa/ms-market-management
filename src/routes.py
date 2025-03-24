from flask import jsonify, make_response
from src.Application.Controllers.user_controller import LoginController


def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return LoginController.login()
