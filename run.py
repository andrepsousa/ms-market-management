from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from src.Config.data_base import init_db
from src.routes import init_routes


jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['JWT_SECRET_KEY'] = '15a1594f9ad60be7a8c9c846f7ec5c3'
    app.config['SECRET_KEY'] = 'a53474c28c456c9e4ceef83c00c14d9'

    init_db(app)

    init_routes(app)

    jwt.init_app(app)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
