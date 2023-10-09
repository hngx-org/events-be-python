from django.db import models
import uuid

from django.contrib.auth.models import BaseUserManager

class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=225, blank=True, null=True)
    email = models.EmailField(unique=True)
    avatar = models.TextField(blank=True, null=True) #change to cloudinary later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_anonymous(self):
        pass
    
    @property
    def is_authenticated(self):
        pass

    def __str__(self):
        return self.name
    