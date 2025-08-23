from flask_restful import Resource, reqparse
from flask import abort
from app.services.config_service import (
    create_or_update_config,
    get_all_configs,
    get_config_by_name,
    delete_config_by_name
)
from mongoengine.errors import DoesNotExist

class ConfigResource(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Name cannot be blank")
        parser.add_argument("value", required=True, help="Value cannot be blank")
        data = parser.parse_args()

        config = create_or_update_config(data["name"], data["value"])
        return {"name": config.name, "value": config.value}, 200

    def get(self):
        configs = get_all_configs()
        return [
            {
                "id": str(c.id),
                "name": c.name,
                "value": c.value,
                "createdAt": c.createdAt.isoformat(),
                "lastUpdatedAt": c.lastUpdatedAt.isoformat()
            }
            for c in configs
        ], 200


class SingleConfigResource(Resource):
    def get(self, name):
        try:
            config = get_config_by_name(name)
            return {
                "id": str(config.id),
                "name": config.name,
                "value": config.value,
                "createdAt": config.createdAt.isoformat(),
                "lastUpdatedAt": config.lastUpdatedAt.isoformat()
            }, 200
        except DoesNotExist:
            abort(404, description=f"Config '{name}' not found")

    def delete(self, name):
        try:
            delete_config_by_name(name)
            return {"message": f"Config '{name}' deleted successfully"}, 200
        except DoesNotExist:
            abort(404, description=f"Config '{name}' not found")