from django.db import IntegrityError, transaction
from django.contrib.auth import get_user
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Coupon, CouponUser
from .serializers import CouponSerializer, CouponUserSerializer
from util.functions import generateRandomSlugCode

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

class CouponUserViewSet(viewsets.ModelViewSet):
    queryset = CouponUser.objects.all()
    serializer_class = CouponUserSerializer

    def create(self, request):
        user = get_user(request)
        request.data['user'] = user.id
        request.data['code'] = generateRandomSlugCode(8)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                coupon = Coupon.objects.select_for_update().get(id=request.data['coupon'])
                self.perform_create(serializer)
                coupon.count -= 1
                coupon.save()

        except IntegrityError as e:
            if 'CHECK constraint failed: count' in str(e):
                return Response({'result' : '쿠폰이 모두 소진되었습니다'}, status=status.HTTP_400_BAD_REQUEST)
            
            elif 'UNIQUE constraint' in str(e):
                return Response({'result' : '이미 쿠폰을 받았습니다'}, status=status.HTTP_400_BAD_REQUEST)
            


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)