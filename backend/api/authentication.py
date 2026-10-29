from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the access token from HttpOnly cookies
    instead of the Authorization header, preventing XSS token theft.
    """
    def authenticate(self, request):
        header = self.get_header(request)
        raw_token = None
        
        if header is not None:
            raw_token = self.get_raw_token(header)
        elif 'access_token' in request.COOKIES:
            raw_token = request.COOKIES.get('access_token')
            
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token