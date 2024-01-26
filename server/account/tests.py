from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from .models import User

from config.testcases import testUser

# 회원 가입 테스트
class SignupAPITest(APITestCase):
    def setUp(self):
        self.signupUrl = reverse("signup")
        testUser['confirm_password'] = testUser['password']
        self.client = APIClient()

    def tearDown(self):
        self.signupUrl = None
        self.client = None

        User.objects.all().delete()

    # 회원 가입 성공
    def testSignupSuccess(self):
        response = self.client.post(self.signupUrl, data=testUser, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 회원 가입 실패 - 이미 등록된 이메일
    def testSignupFail_AlreadyRegistedEmail(self):
        self.client.post(self.signupUrl, data=testUser, format="json")
        response = self.client.post(self.signupUrl, data=testUser, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'user의 email은/는 이미 존재합니다.')

    # 회원 가입 실패 - 비밀번호 불일치
    def testSignupFail_PasswordMismatch(self):
        body = {
            "email": testUser["email"], 
            "password": testUser["password"],
            "confirm_password": "1234"
        }

        response = self.client.post(self.signupUrl, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'][0], '비밀번호가 일치하지 않습니다.')

# 로그인 테스트
class LoginAPITest(APITestCase):
    def setUp(self):
        self.loginUrl = reverse("login")

        self.user = User.objects.create(
            email = testUser["email"],
            password = make_password(testUser["password"])
        )
        
        self.client = APIClient()

    def tearDown(self):
        self.loginUrl = None
        self.user = None
        self.client = None

        User.objects.all().delete()

    # 로그인 성공
    def testLoginSuccess(self):
        response = self.client.post(self.loginUrl, testUser, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'login success')

    # 로그인 실패 - 잘못된 비밀번호
    def testLoginFail_WrongPassword(self):
        body = {
            "email": testUser["email"], 
            "password": "1234"
        }

        response = self.client.post(self.loginUrl, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['result'], '이메일 혹은 비밀번호가 올바르지 않습니다')

    # 로그인 실패 - 등록되지 않은 이메일
    def testLoginFail_NotRegistedEmail(self):
        body = {
            "email": "wrong@test.com", 
            "password": testUser["password"]
        }

        response = self.client.post(self.loginUrl, data=body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['result'], '이메일 혹은 비밀번호가 올바르지 않습니다')

# 로그아웃 테스트
class LogoutAPITest(APITestCase):
    def setUp(self):
        self.loginUrl = reverse("login")
        self.logoutUrl = reverse("logout")

        self.user = User.objects.create(
            email=testUser["email"],
            password=make_password(testUser["password"])
        )

        self.client = APIClient()

    def tearDown(self):
        self.logoutUrl = None
        self.user = None
        self.client = None

        User.objects.all().delete()

    # 로그아웃 성공
    def testLogoutSuccess(self):
        self.client.post(self.loginUrl, testUser, format="json")

        response = self.client.post(self.logoutUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'logout success')

    # 로그아웃 실패 - 로그인 되지 않은 상태
    def testLogoutFail_NotLogin(self):
        response = self.client.post(self.logoutUrl)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)