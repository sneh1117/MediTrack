from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProfileView,PatientViewSet,AssignDoctorView,LoginView
from rest_framework.routers import DefaultRouter

router =DefaultRouter()
router.register(r'patients',PatientViewSet,basename='patients')

urlpatterns = [
       path('register/', RegisterView.as_view(), name='register'),
       path('login/', LoginView.as_view(), name='login'),
       path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
       path('profile/', ProfileView.as_view(), name='profile'),
       path('assign-doctor/',AssignDoctorView.as_view(),name='assign_doctor'),
   ]+router.urls