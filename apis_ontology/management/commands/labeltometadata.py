from django.core.management.base import BaseCommand

from apis_core.apis_labels.models import Label
from apis_core.apis_entities.models import TempEntityClass

class Command(BaseCommand):

    def handle(self, *args, **options):

        for label in Label.objects.all():
            entity = TempEntityClass.objects_inheritance.get_subclass(id=label.temp_entity_id)
            if hasattr(entity, "metadata"):
                if entity.metadata is None:
                    entity.metadata = dict()
                entity.metadata[label.label_type.name] = label.label
                entity.save()
                print(f"Copied label {label.label} to {entity}")
