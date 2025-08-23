from app.models.uncategorized_coin_model import UncategorizedCoin
from mongoengine.errors import DoesNotExist
import datetime
from typing import List

def get_uncategorized_coins_for_today_or_yesterday() -> List[UncategorizedCoin]:
    """
    Get uncategorized coins for today.
    If none, try yesterday.
    If still none, raise DoesNotExist.
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # today’s data
    coins_today = UncategorizedCoin.objects(
        effectiveDate__gte=datetime.datetime(today.year, today.month, today.day),
        effectiveDate__lt=datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=1)
    )

    if coins_today:
        return list(coins_today)

    # yesterday’s data
    coins_yesterday = UncategorizedCoin.objects(
        effectiveDate__gte=datetime.datetime(yesterday.year, yesterday.month, yesterday.day),
        effectiveDate__lt=datetime.datetime(today.year, today.month, today.day)
    )

    if coins_yesterday:
        return list(coins_yesterday)

    raise DoesNotExist("No uncategorized coins found for today or yesterday.")


def create_uncategorized_coins_if_not_exists() -> List[UncategorizedCoin]:
    """
    Check if today's coins exist.
    If yes, return message 'already calculated'.
    If no, create dummy data and return it.
    """
    today = datetime.date.today()
    start_of_day = datetime.datetime(today.year, today.month, today.day)

    # Check if already exists
    coins_today = UncategorizedCoin.objects(
        effectiveDate__gte=start_of_day,
        effectiveDate__lt=start_of_day + datetime.timedelta(days=1)
    )
    if coins_today:
        return None  # Already calculated

    # Otherwise, create dummy data (for now)
    dummy_data = [
        {"name": "BTC", "volatility": 0.12, "volume": 1000000, "riskLevel": 3},
        {"name": "ETH", "volatility": 0.15, "volume": 800000, "riskLevel": 2},
        {"name": "DOGE", "volatility": 0.30, "volume": 500000, "riskLevel": 5},
    ]

    created_coins = []
    for data in dummy_data:
        coin = UncategorizedCoin(
            name=data["name"],
            volatility=data["volatility"],
            volume=data["volume"],
            effectiveDate=start_of_day,
            riskLevel=data["riskLevel"]
        )
        coin.save()
        created_coins.append(coin)

    return created_coins
