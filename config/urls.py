from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/medications/', include('medications.urls')),
    path('api/', include('symptoms.urls')),  # This should be 'api/', not 'api/symptoms/'
]