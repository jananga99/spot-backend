from flask_restful import Resource
from flask import abort
from app.services.selected_coin_service import (
    get_today_selected_coins,
    select_and_update_coins
)
from mongoengine.errors import DoesNotExist

class SelectedCoinResource(Resource):
    def get(self):
        try:
            coins = get_today_selected_coins()
            return {
                "data": [
                    {
                        "id": str(c.id),
                        "name": c.name,
                        "volatility": c.volatility,
                        "volume": c.volume,
                        "riskLevel": c.riskLevel,
                        "effectiveDate": c.effectiveDate.isoformat(),
                        "endDate": c.endDate.isoformat() if c.endDate else None,
                        "createdAt": c.createdAt.isoformat(),
                        "lastUpdatedAt": c.lastUpdatedAt.isoformat()
                    }
                    for c in coins
                ],
                "message": "Selected coins for today retrieved successfully"
            }, 200
        except DoesNotExist:
            abort(404, description="No selected coins found for today")

    def post(self):
        result = select_and_update_coins()
        if result:
            return {
                "data": [],
                "message": "Selected coins updated successfully"
            }, 201
        else:
            return {
                "data": [],
                "message": "No uncategorized coins available for selection today"
            }, 200