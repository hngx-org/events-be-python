from django.conf import settings
from django.db import models
import uuid
class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class User_Groups(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    
