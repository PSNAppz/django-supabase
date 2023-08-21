from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
import jwt

# from .supabase_app import supabase_app

User = get_user_model()

class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Supabase Authentication based Django rest framework authentication class.

    Clients should authenticate by passing a Supabase JWT in the
    "Authorization" HTTP header, prepended with the string "<keyword> " where
    <keyword> is this classes `keyword` string property. For example:

    Authorization:Token xxxxx.yyyyy.zzzzz
    """

    keyword = 'Token'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        if len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            supabase_token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(supabase_token)

    def authenticate_credentials(self, supabase_token):
        try:
            decoded_token = jwt.decode(supabase_token, self.supabase_secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            msg = 'The Supabase token has expired.'
            raise AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = 'The Supabase token is invalid.'
            raise AuthenticationFailed(msg)

        user_id = decoded_token.get('sub')

        if not user_id:
            msg = 'No user ID found in the token.'
            raise AuthenticationFailed(msg)

        # Fetch the user or create a new user if not exist
        try:
            user = User.objects.get(uid=user_id)
        # If a new user was created, you may want to set additional fields
        except User.DoesNotExist:
            # Fetch the user's details from the database
            result = supabase_app.from_('auth.users').select('*').eq('id', user_id).execute()
            supabase_user = result['data'][0]
            user = User.objects.create_user(
                uid=user_id,
                email=supabase_user['email'],
            )

        return (user, decoded_token)


    def authenticate_header(self, request):
        """
        Returns a string that will be used as the value of the WWW-Authenticate
        header in a HTTP 401 Unauthorized response.
        """
        return self.keyword
