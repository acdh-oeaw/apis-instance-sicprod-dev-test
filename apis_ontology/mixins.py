from django.db import models

class MetadataMixin(models.Model):
    metadata = models.JsonField(blank=True, null=True, editable=False)

    class Meta:
        abstract = True
