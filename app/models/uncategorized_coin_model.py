from mongoengine import Document, StringField, IntField, FloatField, DateTimeField, signals
import datetime

class UncategorizedCoin(Document):
    name = StringField(required=True, unique=True)
    volatility = FloatField(required=True)
    volume = FloatField(required=True)
    effectiveDate = DateTimeField(required=True)
    riskLevel = IntField(required=True)
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    lastUpdatedAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'UncategorizedCoin'
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.lastUpdatedAt = datetime.datetime.utcnow()


# Connect signal
signals.pre_save.connect(UncategorizedCoin.pre_save, sender=UncategorizedCoin)