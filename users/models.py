from django.db import models
import uuid
class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    avatar = models.TextField(blank=True, null=True) #change to cloudinary later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name