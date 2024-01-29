from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template import loader

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from .serializers import SignUpSerializer

# 회원가입 View
class SignUpView(APIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인 View
class LogInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'result' : 'login success'}, status=status.HTTP_200_OK)
        else:
            return Response({'result' : '이메일 혹은 비밀번호가 올바르지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)

class LogOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'result' : 'logout success'}, status=status.HTTP_200_OK)
    
def LoginPage(request):
    template = loader.get_template('account/login.html')
    context = {}
    return HttpResponse(template.render(context, request))