from flask import request, jsonify, make_response
from src.Application.Service.user_service import LoginService


class LoginController:
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = LoginService.sign_in(email, password)

        if user:
            return make_response(jsonify({
                "messagem": "Login successful!",
                "user": user.to_dict()
            }), 200)

        else:
            return make_response(jsonify({
                "error": "Invalid credentials"
            }), 400)
