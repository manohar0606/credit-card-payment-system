import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import BlacklistedToken


User = get_user_model()


def get_authenticated_user(request):

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, JsonResponse(
            {"error": "Authorization header is required"},
            status=401
        )

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, JsonResponse(
            {"error": "Invalid Authorization header format"},
            status=401
        )

    token = parts[1]

    # Check whether the token was logged out
    if BlacklistedToken.objects.filter(token=token).exists():
        return None, JsonResponse(
            {"error": "Token has been logged out"},
            status=401
        )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = payload.get("user_id")

        if not user_id:
            return None, JsonResponse(
                {"error": "Invalid token"},
                status=401
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None, JsonResponse(
                {"error": "User not found"},
                status=401
            )

        return user, None

    except jwt.ExpiredSignatureError:
        return None, JsonResponse(
            {"error": "Token has expired"},
            status=401
        )

    except jwt.InvalidTokenError:
        return None, JsonResponse(
            {"error": "Invalid token"},
            status=401
        )