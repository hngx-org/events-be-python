from uuid import uuid4
from datetime import datetime

from django.db import models


from events.models import Events
from users.models import CustomUser
import uuid

def generateUUID():
    return str(uuid.uuid4())


# Create your models here.
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                   default=None)

    def __str__(self) -> str:
        return str(self.id)
