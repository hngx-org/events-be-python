from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from social_django.models import UserSocialAuth
from django.contrib.auth.models import AbstractUser

class CustomUser(models.Model):
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = models.CharField(max_length=30, unique=True)  # Ensure username is unique
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    # Add any additional fields or methods you need for your custom user model

    def __str__(self):
        return self.username  # Customize the string representation of the user

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


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
