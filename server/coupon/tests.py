from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APITransactionTestCase, APIClient

from account.models import User
from work.models import Work
from coupon.models import Coupon

from config.testcases import testUser, testWorks

# 쿠폰 발급 테스트
class CouponAPITest(APITransactionTestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            email = testUser["email"],
            password = make_password(testUser["password"])
        )

        self.client.login(email=testUser["email"], password=testUser["password"])

        self.works = [ Work.objects.create(**work) for work in testWorks ]

        self.coupon = Coupon.objects.create(
            name = "TEST COUPON 1",
            count = 5
        )

        self.couponUrl = reverse("couponuser-list")        

    def tearDown(self):
        self.client = None
        self.works = None
        self.coupon = None
        self.couponUrl = None
        
        User.objects.all().delete()
        Work.objects.all().delete()
        Coupon.objects.all().delete()

    # 쿠폰 발급 성공
    def testCouponIssuingSuccess(self):
        data = {
            "coupon" : self.coupon.id,
            "work" : self.works[0].id
        }

        response = self.client.post(self.couponUrl, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['coupon'], data['coupon'])
        self.assertEqual(response.data['work'], data['work'])
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(len(response.data['code']), 8)
        self.assertEqual(response.data['is_used'], False)


    # 쿠폰 발급 실패 - 쿠폰 소진
    def testCouponIssuingFail_OutOfCoupon(self):
        data = [
            {
                "coupon" : self.coupon.id,
                "work" : work.id
            }
            for work in self.works
        ]

        for i in range(5):
            self.client.post(self.couponUrl, data=data[i], format="json")

        response = self.client.post(self.couponUrl, data=data[5], format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['result'], '쿠폰이 모두 소진되었습니다')

    # 쿠폰 발급 실패 - 이미 발급된 쿠폰
    def testCouponIssuingFail_AlreadyIssued(self):
        data = {
            "coupon" : self.coupon.id,
            "work" : 1
        }

        successResponse = self.client.post(self.couponUrl, data=data, format="json")
        self.assertEqual(successResponse.status_code, status.HTTP_201_CREATED)

        failResponse = self.client.post(self.couponUrl, data=data, format="json")
        self.assertEqual(failResponse.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(failResponse.data['result'], '이미 쿠폰을 받았습니다')
