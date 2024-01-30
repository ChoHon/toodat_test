from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from work.views import WorkViewSet
from coupon.views import CouponViewSet, CouponUserViewSet

router = DefaultRouter()
router.register(r'work', WorkViewSet, basename='work')
router.register(r'coupon', CouponViewSet, basename='coupon')
router.register(r'couponuser', CouponUserViewSet, basename='couponuser')

urlpatterns = [
    path('', include(router.urls)),
    path('account/', include('account.urls')),
    path('event/', include('event.urls')),

    path('admin/', admin.site.urls),
]