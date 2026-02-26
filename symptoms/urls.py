from rest_framework.routers import DefaultRouter
from .views import SymptomViewSet,MoodLogViewSet
from .dashboard import DashboardView
from django.urls import path

router = DefaultRouter()
router.register(r'symptoms', SymptomViewSet, basename='symptoms')
router.register(r'moods',MoodLogViewSet,basename='moods')

urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
]+router.urls