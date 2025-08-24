import datetime
from app.models.selected_coin_model import SelectedCoin
from app.models.uncategorized_coin_model import UncategorizedCoin

def get_today_selected_coins():
    today = datetime.date.today()
    return SelectedCoin.objects(effectiveDate=today, endDate=None)

def select_and_update_coins():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    # Step 1: Get uncategorized coins for today
    uncategorized = UncategorizedCoin.objects(effectiveDate=today)
    if not uncategorized:
        return False  # No uncategorized coins available
    
    # Step 2: Dummy selection logic (pick top 3 by volume for now)
    selected = sorted(uncategorized, key=lambda c: c.volume, reverse=True)[:3]
    selected_names = {c.name for c in selected}

    # Step 3: Update DB for selected coins
    for coin in selected:
        latest_record = (
            SelectedCoin.objects(name=coin.name)
            .order_by("-effectiveDate")
            .first()
        )

        if latest_record and latest_record.endDate is None:
            if latest_record.volatility != coin.volatility or latest_record.volume != coin.volume or latest_record.riskLevel != coin.riskLevel:
                # Update existing record, do not change effectiveDate
                latest_record.volatility = coin.volatility
                latest_record.volume = coin.volume
                latest_record.riskLevel = coin.riskLevel
                latest_record.save()
        else:
            # Insert new record
            SelectedCoin(
                name=coin.name,
                volatility=coin.volatility,
                volume=coin.volume,
                riskLevel=coin.riskLevel,
                effectiveDate=today,
                endDate=None
            ).save()

    # Step 4: Expire non-selected coins
    non_selected = SelectedCoin.objects(endDate=None, effectiveDate__lte=today)
    for record in non_selected:
        if record.name not in selected_names:
            record.endDate = yesterday
            record.lastUpdatedAt = datetime.datetime.utcnow()
            record.save()
            
    return True
