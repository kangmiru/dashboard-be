# authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Misalnya, kita menggunakan token dari header Authorization
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None  # Tidak ada header Authorization

        # Split header untuk mendapatkan token
        _, token = auth_header.split()

        # Lakukan validasi token atau logika otentikasi kustom
        try:
            user_model = get_user_model()
            user = user_model.objects.get(password=token)  # Sesuaikan dengan logika otentikasi Anda
        except user_model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        return (user, None)
