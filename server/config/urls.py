from django.urls import path, include
from rest_framework.routers import DefaultRouter

from work.views import WorkViewSet
from coupon.views import CouponViewSet

router = DefaultRouter()
router.register(r'work', WorkViewSet, basename='work')
router.register(r'coupon', CouponViewSet, basename='coupon')

urlpatterns = [
    path('', include(router.urls)),
    path('account/', include('account.urls')),
]
