from rest_framework import routers
from django.urls import path, include
from .views import BookViewSet, BorrowerViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'borrowers', BorrowerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
