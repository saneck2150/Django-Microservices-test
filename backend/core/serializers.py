from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import UploadedFile

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "full_name", "date_joined"]
        read_only_fields = ["id", "date_joined", "username"]

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)  # 👈 делаем email необязательным

    class Meta:
        model = CustomUser
        fields = ["username", "email", "full_name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(**validated_data)
        return user


ALLOWED_TYPES = [
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/plain",
    "text/x-python",
]

class UploadedFileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = UploadedFile
        fields = ["id", "filename", "content_type", "uploaded_at", "file"]
        read_only_fields = ["id", "filename", "content_type", "uploaded_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        upload = validated_data["file"]

        return UploadedFile.objects.create(
            user=user,
            filename=upload.name,
            content_type=upload.content_type,
            content=upload.read()
        )

class UploadedFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ["id", "filename", "content_type", "uploaded_at"]
