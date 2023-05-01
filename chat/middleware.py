from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.auth import AuthMiddleware
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

"""[summary]
plucks the JWT access token from the query string and retrieves the associated user.
  Once the WebSocket connection is opened, all messages can be sent and received without
  verifying the user again. Closing the connection and opening it again 
  requires re-authorization.
for example: 
ws://localhost:8000/<route>/?token=<token_of_the_user>

"""


@database_sync_to_async
def get_user(scope):
    close_old_connections()
    token = get_token(scope)
    if not token:
        return AnonymousUser()
    try:
        access_token = AccessToken(token)
        user = User.objects.get(id=access_token['user_id'])
    except Exception as exception:
        return AnonymousUser()
    if not user.is_active:
        return AnonymousUser()
    return user


class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(scope)


def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))

def get_token(s):
    for i in s['headers']:
        if i[0].decode() == 'authorization':
            return i[1].decode().split()[1]
    