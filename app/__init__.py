from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    load_dotenv()
    
    # Configure secret key
    app.config['SECRET_KEY'] = os.urandom(24)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app