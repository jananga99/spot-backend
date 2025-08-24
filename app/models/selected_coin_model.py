from mongoengine import Document, StringField, FloatField, DateTimeField, signals, DateField, IntField
import datetime

class SelectedCoin(Document):
    name = StringField(required=True)
    volatility = FloatField(required=True)
    volume = FloatField(required=True)
    riskLevel = IntField(required=True)
    effectiveDate = DateField(required=True)   # when it became selected
    endDate = DateField(null=True)             # when selection ended
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
