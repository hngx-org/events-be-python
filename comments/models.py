from uuid import uuid4

from django.db import models


from events.models import Events
from users.models import CustomUser


# Create your models here.
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = models.CharField(max_length=255)
    created_at = models.DateField()
    updated_at = models.DateField()
    event_id = models.ForeignKey(Events, on_delete=models.PROTECT)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                   default=None)

    def __str__(self) -> str:
        return str(self.id)
