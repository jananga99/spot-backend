from mongoengine import Document, StringField, FloatField, DateTimeField, signals
import datetime

class SelectedCoin(Document):
    name = StringField(required=True, unique=True)
    volatility = FloatField(required=True)
    volume = FloatField(required=True)
    effectiveDate = DateTimeField(required=True)
    endDate = DateTimeField(required=False, null=True)
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    lastUpdatedAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'SelectedCoin'
    }
    
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.lastUpdatedAt = datetime.datetime.utcnow()

# Connect signal
signals.pre_save.connect(SelectedCoin.pre_save, sender=SelectedCoin)
