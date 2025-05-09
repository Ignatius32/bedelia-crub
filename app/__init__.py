# Inicializador de paquete para app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Inicializar extensiones
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object('config')
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Contexto global para las plantillas
    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.now()}
      # Registrar blueprints
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    from app.admin import admin as admin_blueprint
    from app.api import api as api_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(api_blueprint)
    
    return app
