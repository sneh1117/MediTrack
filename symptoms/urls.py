from rest_framework.routers import DefaultRouter
from .views import SymptomViewSet

router = DefaultRouter()
router.register(r'', SymptomViewSet, basename='symptoms')


urlpatterns = router.urls