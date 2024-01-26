from django.urls import path, include
from rest_framework.routers import DefaultRouter

from work.views import WorkViewSet

router = DefaultRouter()
router.register(r'work', WorkViewSet, basename='work')

urlpatterns = [
    path('', include(router.urls)),
    path('account/', include('account.urls')),
]
