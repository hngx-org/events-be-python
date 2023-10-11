from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from social_django.models import UserSocialAuth

from django.db import models


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    admin = models.ForeignKey('social_django.UserSocialAuth', on_delete=models.CASCADE, related_name='admin_groups', db_column='user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'custom_group_table_name'
            
            
class User_Groups(models.Model):
    user = models.ForeignKey('social_django.UserSocialAuth', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    
