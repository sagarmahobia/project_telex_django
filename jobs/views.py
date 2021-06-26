# Create your views here.
from datetime import datetime

from app.models import Entity
from services import rest_client


def execute():
    entities = Entity.objects.filter(fetched=False)
    for entity in entities:
        title, description, image, subscribers = rest_client.get_info_by_id(entity.entity_id, entity.entity_type)
        entity.title = title

        entity.description = description
        entity.image = image
        entity.subscribers = subscribers
        entity.fetched = True
        entity.last_updated = datetime.now()
        entity.save()
