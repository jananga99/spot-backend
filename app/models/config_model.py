from mongoengine import Document, StringField, DateTimeField, signals
import datetime

class Config(Document):
    name = StringField(required=True, unique=True)
    value = StringField(required=True)
    createdAt = DateTimeField(default=datetime.datetime.utcnow)
    lastUpdatedAt = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'Config'
    }
    
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.lastUpdatedAt = datetime.datetime.utcnow()

# Connect signal
signals.pre_save.connect(Config.pre_save, sender=Config)
