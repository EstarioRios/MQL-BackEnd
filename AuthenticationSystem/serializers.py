from rest_framework import serializers
from .models import CustomUser, Order


class CustomUserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "user_type",
            "active_mode",
        ]


class CustomUserDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "user_type",
            "email",
            "phone_number",
            "active_mode",
        ]


class OrderListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "title",
            "tools_description",
        ]


class OrderDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["__all__"]
