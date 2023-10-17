from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from social_django.models import UserSocialAuth
from django.contrib.auth.models import AbstractUser

class CustomUser(models.Model):
    email = models.EmailField(unique=True)  # Ensure email is unique
    username = models.CharField(max_length=30, unique=True)  # Ensure username is unique
    profile_picture = models.CharField(max_length=1000)

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

        
    def save(self, *args, **kwargs):
        super(User_Groups, self).save(args, **kwargs)
        if True:
            message = f"{self.admin} has added you to {self.group.group_name}"
        
        Notification.objects.create(user=self.user, admin=self.group.admin, message=message)
        return message

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