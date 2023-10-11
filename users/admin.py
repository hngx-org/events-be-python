from django.contrib import admin
from .models import User_Groups,Group,CustomUser
# Register your models here.
admin.site.register(User_Groups)
admin.site.register(Group)
admin.site.register(CustomUser)