from app.models.config_model import Config
from mongoengine.errors import DoesNotExist
from typing import List

def create_or_update_config(name: str, value: str) -> Config:
    """
    Create a new Config if it doesn't exist, otherwise update the existing one.
    """
    config = Config.objects(name=name).first()
    if config:
        config.value = value
    else:
        config = Config(name=name, value=value)
    config.save()
    return config


def get_all_configs() -> List[Config]:
    """
    Retrieve all Config documents.
    """
    return list(Config.objects)


def get_config_by_name(name: str) -> Config:
    """
    Retrieve a Config by name or raise DoesNotExist.
    """
    return Config.objects.get(name=name)


def delete_config_by_name(name: str) -> None:
    """
    Delete a Config by name or raise DoesNotExist.
    """
    config = Config.objects.get(name=name)  # raises DoesNotExist if not found
    config.delete()