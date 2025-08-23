from flask import Flask
from flask_restful import Api
from mongoengine import connect
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # # Connect to MongoDB
    connect(host=app.config['MONGO_URI'])
    api = Api(app)
    
    # Import routes
    from app.routes.health import HealthResource
    api.add_resource(HealthResource, '/health')
    
    return app
