# permissions.py
from rest_framework import permissions
from social_django.models import UserSocialAuth

class IsAuthenticatedSSO(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated through SSO
        sso_auth = request.user.social_auth.filter(provider='google-oauth2').first()
        if sso_auth:
            # Automatically authenticate the user
            request.user = sso_auth.user
            return True
        else:
            return False

