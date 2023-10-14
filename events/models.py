from django.db import models
from users.models import *
import uuid
<<<<<<< HEAD
=======
from social_django.models import UserSocialAuth
from users.models import CustomUser
>>>>>>> 15c9afced6e20341d636111aea7843a51b0a0a2e

# Create your models here.
class Events(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
<<<<<<< HEAD
    creator = models.ForeignKey(User, models.CASCADE, blank=True, null=True)
=======
    creator = models.ForeignKey(CustomUser, models.CASCADE, blank=True, null=True)
>>>>>>> 15c9afced6e20341d636111aea7843a51b0a0a2e
    group = models.ForeignKey(Group, models.CASCADE, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)


    def __str__(self):
        return self.title
    

class InterestinEvents(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
<<<<<<< HEAD
    user = models.ForeignKey(User, on_delete=models.CASCADE)
=======
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
>>>>>>> 15c9afced6e20341d636111aea7843a51b0a0a2e
    create_at = models.DateTimeField(auto_now_add=True)

