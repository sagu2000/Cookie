from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class CookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.COOKIES.get("auth_token")
        if not auth_token:
            return None
        try:
            user = User.objects.get(id=auth_token)
            return (user, None)
        except ObjectDoesNotExist:
            return None
