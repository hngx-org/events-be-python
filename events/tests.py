from django.test import TestCase
from rest_framework.test import APIClient,APITestCase
from .models import Events
# Create your tests here.
# class TestEvents(APITestCase):
#     def setUp(self):
#         self.client=APIClient()
#         event=Events.objects.create()
#         self.request.id=