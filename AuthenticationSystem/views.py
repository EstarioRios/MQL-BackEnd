from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import CustomUser, Order
from .serializers import (
    CustomUserDetailSerializers,
    CustomUser,
    Order,
    OrderDetailSerializers,
    OrderListSerializers,
    CustomUserListSerializers,
)


# Generate JWT access and refresh tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user=user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


# Dashboard Response Generator
def choose_dashboard(user, tokens, msg="Login successful", remember=False):
    if not tokens:
        return Response(
            {
                "user_type": user.user_type,
                "success": msg,
                "user": CustomUserDetailSerializers(user).data,
            },
            status=status.HTTP_200_OK,
        )
    else:
        if remember == True:
            return Response(
                {
                    "user_type": user.user_type,
                    "success": msg,
                    "tokens": tokens,
                    "user": CustomUserDetailSerializers(user).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "user_type": user.user_type,
                    "success": msg,
                    "user": CustomUserDetailSerializers(user).data,
                },
                status=status.HTTP_200_OK,
            )


# Admin-only signup view
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):

    # Extract new user data
    user_user_type = request.data.get("user_type")
    user_email = request.data.get("email")
    user_phone_number = request.data.get("phone_number")
    user_password = request.data.get("password")
    user_first_name = request.data.get("first_name")
    user_last_name = request.data.get("last_name")

    # Check for required fields
    if not all(
        [
            user_user_type,
            user_phone_number,
            user_email,
            user_password,
            user_first_name,
            user_last_name,
        ]
    ):
        return Response(
            {
                "error": "All fields (user_user_type, user_phone_number, user_email, user_password, user_first_name, user_last_name) are required."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if user_user_type == "normal":
        try:
            if CustomUser.objects.filter(email=user_email).exists():
                return Response(
                    {"error": f"email: {user_email} is already exist"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            try:
                user = CustomUser.objects.create_normal(
                    user_type="normal",
                    phone_number=user_phone_number,
                    email=user_email,
                    first_name=user_first_name,
                    last_name=user_last_name,
                    password=user_password,
                )
            except ValueError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return Response(
                {
                    "msg": "user created",
                    "user": CustomUserDetailSerializers(user).data,
                    "tokens": get_tokens_for_user(user),
                }
            )

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


# Manual login if JWT not present
@api_view(["POST"])
@permission_classes([AllowAny])
def manual_login(request, remember):
    user_email = request.data.get("email")
    user_password = request.data.get("password")

    if not user_email or not user_password:
        return Response(
            {"error": "email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = CustomUser.objects.get(email=user_email)
        if user.check_password(user_password):
            return choose_dashboard(
                user, tokens=get_tokens_for_user(user), remember=remember
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Login view: prefer JWT, fallback to manual login
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    remember = request.data.get("remember")
    if not remember:
        remember = False

    try:

        user_auth = JWTAuthentication().authenticate(request)
        if not user_auth:
            return manual_login(request, remember=remember)

        else:
            user, _ = user_auth
            return choose_dashboard(user, tokens=None, remember=False)

    except AuthenticationFailed:
        return manual_login(request, remember=remember)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_admin(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not ok"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    password = request.data.get("password")
    phone_number = request.data.get("phone_number")

    if not all([first_name, last_name, email, password, phone_number]):
        return Response(
            {
                "error": "first_name, last_name, email, password, phone_number fields are requirements"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, _ = user_auth
    try:
        if user.user_type != "admin":
            return Response(
                {"error": "you are not allowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = CustomUser.objects.create_admin(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
            )
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sub_order(request):
    user_auth = JWTAuthentication().authenticate(request)
    if not user_auth:
        return Response(
            {"error": "your JWT is not ok"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, _ = user_auth

    order_title = request.data.get("title")
    order_owner = user
    order_description = request.data.get("description")
    order_tools_description = request.data.get("tools_description")

    if not all(
        [
            order_description,
            order_title,
            order_tools_description,
            order_owner,
        ]
    ):
        return Response(
            {
                "error": "order_description, order_title, order_tools_description, order_owner are requiremented"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        order = Order.objects.create(
            title=order_title,
            owner=order_owner,
            description=order_description,
            tools_description=order_tools_description,
        )
        order.save()
    except ValueError as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST,
        )
