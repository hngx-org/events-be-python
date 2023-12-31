from uuid import uuid4
from datetime import datetime

from django.db import models


from events.models import Events
from social_django.models import UserSocialAuth
import uuid

from users.models import CustomUser

def generateUUID():
    return str(uuid.uuid4())


# Create your models here.
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)
    event_id = models.ForeignKey(Events, on_delete=models.CASCADE)
    created_by = models.ForeignKey(CustomUser, models.CASCADE, blank=True, null=True)
    picture = models.ImageField(upload_to='comment_pictures/', null=True, blank=True)
    voice_note = models.FileField(upload_to='comment_voice_notes/', null=True, blank=True)


    def __str__(self) -> str:
        return str(self.id)
