from rest_framework import serializers
from .models import CustomUser, Order


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_type",
            "phone_number",
            "email",
            "active_mode",
        ]
        read_only_fields = ["id", "user_type"]


class CreateNormalUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]

    def create(self, validated_data):
        return CustomUser.objects.create_normal(**validated_data)


class CreateAdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
        ]

    def create(self, validated_data):
        return CustomUser.objects.create_admin(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "title",
            "description",
            "tools_description",
            "owner",
        ]
        read_only_fields = ["id", "owner"]
