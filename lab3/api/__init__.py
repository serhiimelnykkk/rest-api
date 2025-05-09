from flask import Flask
from .config import Config
from .models import db # Імпортуємо db з models
from .routes import main_bp # Будемо створювати blueprint для маршрутів

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app) # Ініціалізуємо db з додатком

    # Реєструємо Blueprint
    app.register_blueprint(main_bp)

    return app