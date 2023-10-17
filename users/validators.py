import binascii
from rest_framework import serializers
import os

def validate_base64(value):
    try:
        import base64
        # Attempt to decode the input value as Base64
        base64.b64decode(value)
    except (binascii.Error, TypeError):
        raise serializers.ValidationError("Invalid Base64 format")
    
