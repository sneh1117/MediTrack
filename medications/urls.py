from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicationViewSet
from .adherence import AdherenceView

router = DefaultRouter()
router.register(r'', MedicationViewSet, basename='medications')

urlpatterns = [
    path('adherence/',AdherenceView.as_view(),name='adherence'),
]+router.urls