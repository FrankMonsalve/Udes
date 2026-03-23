import os
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    # Cargar el archivo .env desde la raiz del proyecto
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
    
    app = Flask(__name__)
    print("DB URI:", repr(app.config.get("SQLALCHEMY_DATABASE_URI")))
    
    # Priorizar DATABASE_URL del entorno, si no usar el archivo en la raiz del proyecto
    # El archivo de la base de datos se ubicará en la raíz del proyecto
    default_db_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'udes_inscripciones.db'))
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg://udes_admin:udes_secure_pass_2024@127.0.0.1:5432/udes_inscripciones"
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///' + default_db_path)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    
    # Configuracion de correo (Gmail)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Configuración de CORS abierta para simplificar el desarrollo sin seguridad
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Registro de rutas e importaciones locales
    from routes import main_bp
    app.register_blueprint(main_bp)
    
    # Registro de comandos CLI
    from commands import seed_db_command
    app.cli.add_command(seed_db_command)

    return app
