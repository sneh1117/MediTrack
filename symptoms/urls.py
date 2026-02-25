from rest_framework.routers import DefaultRouter
from .views import SymptomViewSet
from django.urls import path

router = DefaultRouter()
router.register(r'symptoms', SymptomViewSet, basename='symptoms')

urlpatterns = router.urls