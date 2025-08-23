from flask_restful import Resource
from flask import abort
from app.services.uncategorized_coin_service import (
    get_uncategorized_coins_for_today_or_yesterday,
    create_uncategorized_coins_if_not_exists
)
from mongoengine.errors import DoesNotExist

class UncategorizedCoinResource(Resource):
    def get(self):
        try:
            coins = get_uncategorized_coins_for_today_or_yesterday()
            return {
                "data": [
                    {
                        "id": str(c.id),
                        "name": c.name,
                        "volatility": c.volatility,
                        "volume": c.volume,
                        "riskLevel": c.riskLevel,
                        "effectiveDate": c.effectiveDate.isoformat(),
                        "createdAt": c.createdAt.isoformat(),
                        "lastUpdatedAt": c.lastUpdatedAt.isoformat()
                    }
                    for c in coins
                ],
                "message": "Uncategorized coins retrieved successfully"
            }, 200
        except DoesNotExist:
            abort(404, description="No uncategorized coins found for today or yesterday")

    def post(self):
        coins = create_uncategorized_coins_if_not_exists()
        if coins is None:
            return {
                "data": [],
                "message": "Uncategorized coins for today already calculated"
            }, 200

        return {
            "data": [
                {
                    "id": str(c.id),
                    "name": c.name,
                    "volatility": c.volatility,
                    "volume": c.volume,
                    "riskLevel": c.riskLevel,
                    "effectiveDate": c.effectiveDate.isoformat(),
                    "createdAt": c.createdAt.isoformat(),
                    "lastUpdatedAt": c.lastUpdatedAt.isoformat()
                }
                for c in coins
            ],
            "message": "Uncategorized coins created successfully"
        }, 201
