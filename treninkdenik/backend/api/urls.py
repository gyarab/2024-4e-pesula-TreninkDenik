from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UzivatelViewSet, TreninkViewSet

router = DefaultRouter()
router.register(r'uzivatele', UzivatelViewSet, basename='uzivatel')
router.register(r'treninky', TreninkViewSet, basename='trenink')

urlpatterns = [
    path('', include(router.urls)),
]