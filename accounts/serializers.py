from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'first_name', 'last_name', 'bio', 'photo', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

    def get_name(self, obj):
        return obj.get_display_name()

    def get_photo(self, obj):
        request = self.context.get('request')
        avatar_url = obj.get_avatar_url()
        if request and avatar_url.startswith('/media/'):
            return request.build_absolute_uri(avatar_url)
        return avatar_url


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False)
    bio = serializers.CharField(required=False, allow_blank=True, default='')
    avatar = serializers.ImageField(required=False, allow_null=True)

    def validate_email(self, value):
        email = value.strip().lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return email

    def validate(self, data):
        confirm = data.get('confirm_password')
        if confirm and data['password'] != confirm:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    remember = serializers.BooleanField(required=False, default=False)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150, required=False)
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['name', 'bio', 'avatar']

    def update(self, instance, validated_data):
        name = validated_data.pop('name', None)
        if name:
            parts = name.strip().split(' ', 1)
            instance.first_name = parts[0]
            instance.last_name = parts[1] if len(parts) > 1 else ''
        if 'bio' in validated_data:
            instance.bio = validated_data['bio']
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
        instance.save()
        return instance

