from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
                  'twitter': 'twitter', 'email': 'email'}


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='authentication_users_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='authentication_users_user_permissions'
    )

    # class Meta:
    #     app_label = 'auth'
    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class Group(models.Model):
    group_name = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Groupadmin', db_column='user_id')
    image = models.ImageField(upload_to='group_images/',blank=True, null=True)
    friends = models.ManyToManyField(User,related_name='Groupfriends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Group_table'
            
            
class UserGroups(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, )
    
    def __str__(self):
        return f"{self.group.group_name}"
