from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from social_django.models import UserSocialAuth

from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    admin = models.ForeignKey(UserSocialAuth, on_delete=models.CASCADE,related_name='Groupadmin', db_column='user_id')
    image = models.ImageField(upload_to='group_images/',blank=True, null=True)
    friends = models.ManyToManyField(UserSocialAuth,related_name='Groupfriends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'custom_group_table_name'
            
            
class User_Groups(models.Model):
    user = models.ForeignKey(UserSocialAuth,on_delete=models.CASCADE, )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, )
    
    def __str__(self):
        return f"{self.group.group_name}"