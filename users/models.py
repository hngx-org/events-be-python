from django.conf import settings
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser



class CustomUserManager(BaseUserManager):
    """Manager of the user email"""
    
    def create_user(self, email, password=None, **extra_fields):
        """create_user returns a user 
        
        args: (email)
              (password)
        returns: a new user

        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        """create_user returns a user 
        
        args: (email)
              (password)
        returns: a new superuser

        """
        
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("verified", True)

        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=225, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False,null=True)
    avatar = models.TextField(blank=True, null=True) #change to cloudinary later
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

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
    
