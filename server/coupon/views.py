from django.db import IntegrityError
from django.contrib.auth import get_user
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Coupon
from .serializers import CouponSerializer

from util.functions import generateRandomSlugCode

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def create(self, request):
        user = get_user(request)
        request.data['user'] = user.id
        request.data['code'] = generateRandomSlugCode(8)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response({'result' : '이미 쿠폰을 받았습니다'}, status=status.HTTP_409_CONFLICT)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)