from uuid import uuid4
from datetime import datetime

from django.db import models


from events.models import Events
import uuid
from users.models import *

def generateUUID():
    return str(uuid.uuid4())


# Create your models here.
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
<<<<<<< HEAD
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   default=None)
=======
    created_by = models.ForeignKey(UserSocialAuth, models.CASCADE, blank=True, null=True)
>>>>>>> 15c9afced6e20341d636111aea7843a51b0a0a2e
    picture = models.ImageField(upload_to='comment_pictures/', null=True, blank=True)
    voice_note = models.FileField(upload_to='comment_voice_notes/', null=True, blank=True)


    def __str__(self) -> str:
        return str(self.id)
