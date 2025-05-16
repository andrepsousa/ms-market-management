from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_migrate import Migrate
from src.Config.data_base import init_db, db
from src.routes import main_bp
from src.product_routes import product_bp
import os
from dotenv import load_dotenv


load_dotenv()

jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    init_db(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    jwt.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()


with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
