from flask import Flask
from flask_restful import Api
from mongoengine import connect
from app.config import Config

from app.routes.health import HealthResource
from app.routes.config_route import ConfigResource, SingleConfigResource
from app.routes.uncategorized_coin_route import UncategorizedCoinResource
from app.routes.selected_coin_route import SelectedCoinResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # # Connect to MongoDB
    connect(host=app.config['MONGO_URI'])
    api = Api(app)
    
    # Import routes
    api.add_resource(HealthResource, '/health')
    api.add_resource(ConfigResource, '/config')
    api.add_resource(SingleConfigResource, '/config/<string:name>')
    api.add_resource(UncategorizedCoinResource, '/uncategorized-coins')
    api.add_resource(SelectedCoinResource, "/selected-coins")
    
    return app
