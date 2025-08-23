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
        return {
            "data": {
                "id": str(config.id),
                "name": config.name,
                "value": config.value,
                "createdAt": config.createdAt.isoformat(),
                "lastUpdatedAt": config.lastUpdatedAt.isoformat()
            },
            "message": "Config created or updated successfully"
        }, 200

    def get(self):
        configs = get_all_configs()
        return {
            "data": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "value": c.value,
                    "createdAt": c.createdAt.isoformat(),
                    "lastUpdatedAt": c.lastUpdatedAt.isoformat()
                }
                for c in configs
            ],
            "message": "Configs retrieved successfully"
        }, 200


class SingleConfigResource(Resource):
    def get(self, name):
        try:
            config = get_config_by_name(name)
            return {
                "data": {
                    "id": str(config.id),
                    "name": config.name,
                    "value": config.value,
                    "createdAt": config.createdAt.isoformat(),
                    "lastUpdatedAt": config.lastUpdatedAt.isoformat()
                },
                "message": "Config retrieved successfully"
            }, 200
        except DoesNotExist:
            abort(404, description={"data": None, "message": f"Config '{name}' not found"})

    def delete(self, name):
        try:
            delete_config_by_name(name)
            return {
                "data": None,
                "message": f"Config '{name}' deleted successfully"
            }, 200
        except DoesNotExist:
            abort(404, description={"data": None, "message": f"Config '{name}' not found"})
