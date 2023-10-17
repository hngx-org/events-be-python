from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from social_django.models import UserSocialAuth
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='Groupadmin', db_column='user_id')
    image = models.ImageField(upload_to='group_images/',blank=True, null=True)
    friends = models.ManyToManyField(CustomUser,related_name='Groupfriends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Group_table'
    
            
class User_Groups(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, )
    
    def __str__(self):
        return f"{self.group.group_name}"
    
    @receiver(post_save, sender=Group)
    def create_user_groups(sender, instance, created, **kwargs):
        if created:
            user_group = User_Groups(group=instance, user=instance.admin)  # Assuming you want to associate the admin with the new group
            user_group.save()

            message = f"{user_group.group.admin} has added you to {user_group.group.group_name}"

            Notification.objects.create(user=user_group.user, admin=user_group.group, message=message)


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )
    admin = models.ForeignKey(Group, on_delete=models.CASCADE,)
    message = models.TextField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False)


class Preferences(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    appearance = models.CharField(max_length=20, default="light")
    language = models.CharField(max_length=225, default='english')
    region = models.CharField(max_length=225, default="Lagos")