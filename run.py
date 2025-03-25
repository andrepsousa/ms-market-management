from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from src.Config.data_base import init_db
from src.routes import init_routes
import os


jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    init_db(app)

    init_routes(app)

    jwt.init_app(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
