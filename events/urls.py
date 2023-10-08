from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'sort/products', basename='product-sort')

urlpatterns = [
    path('api/', include(router.urls)),
]