from rest_framework.authentication import SessionAuthentication

class CustomSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        user = getattr(request._request, 'user', None)

        if not user or not user.is_active:
            return None

        return (user, None)